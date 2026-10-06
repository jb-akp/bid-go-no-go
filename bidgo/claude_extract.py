"""Optional: let Claude read the passages instead of the regex extractor.

Turned on with BIDGO_EXTRACTOR=claude (needs ANTHROPIC_API_KEY). Claude must return, for every
field, the value, the passage id it came from and the exact quote. Nothing it says is trusted:
each answer is checked against the passage text, and anything the cited line doesn't support is
rejected and listed in the memo. A rejected field counts as missing, so it can only push the
recommendation toward HOLD, never toward GO.
"""
import json
import os

from .extract import SCALARS, normalize, supports

MODEL = os.environ.get("BIDGO_MODEL", "claude-sonnet-5")

SYSTEM = (
    "You read construction bid packages for an electrical and low-voltage contractor. "
    "For each field, copy the value only if a passage states it, give that passage's id, and copy "
    "the exact words from the passage as the quote. If no passage states it, return null for value, "
    "passage_id and quote. Do not infer, estimate or combine passages. "
    "Money as written (e.g. $840,000). Percentages as written (e.g. 10%). "
    "prevailing_wage and prebid_mandatory: 'true' or 'false'."
)


def schema():
    item = {
        "type": "object",
        "properties": {
            "value": {"type": ["string", "null"]},
            "passage_id": {"type": ["string", "null"]},
            "quote": {"type": ["string", "null"]},
        },
        "required": ["value", "passage_id", "quote"],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {f: item for f in SCALARS},
        "required": list(SCALARS),
        "additionalProperties": False,
    }


def verify(passages, answers):
    """Keep only answers whose quote is really in the cited passage and really says the value."""
    facts, rejected = {}, []
    for field in SCALARS:
        a = answers.get(field) or {}
        facts[field] = None
        if a.get("value") is None:
            continue
        cite = {"id": a.get("passage_id") or "", "quote": a.get("quote") or ""}
        text = passages.get(cite["id"])
        if not text:
            why = "cited passage does not exist"
        elif not cite["quote"] or " ".join(cite["quote"].lower().split()) not in " ".join(text.lower().split()):
            why = "quote is not in the cited passage"
        elif not supports(field, a["value"], cite["quote"]):
            why = "quote does not state this value"
        else:
            facts[field] = {"value": normalize(field, a["value"]), "cite": {"id": cite["id"], "quote": text}}
            continue
        rejected.append({"field": field, "value": a["value"], "cite": cite, "why": why})
    return facts, rejected


def claude_scalars(passages):
    import anthropic

    client = anthropic.Anthropic()
    body = "\n".join(f"[{pid}] {text}" for pid, text in passages.items())
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=SYSTEM,
        output_config={"format": {"type": "json_schema", "schema": schema()}},
        messages=[{"role": "user", "content": f"Fields: {', '.join(SCALARS)}\n\nPassages:\n{body}"}],
    )
    answers = json.loads(next(b.text for b in resp.content if b.type == "text"))
    return verify(passages, answers)

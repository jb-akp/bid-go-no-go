"""Step 2: pull the commercial and technical facts out of the passages.

Every fact is {"value": ..., "cite": {"id": "<file>:<line>", "quote": "<text from that line>"}},
or None when the package does not state it. The default extractor is plain regex so the demo runs
with no API key and the tests are reproducible. claude_extract.py is the optional model path; its
answers go through supports() below and are dropped if the cited line doesn't back them up.
"""
import re

from .ingest import norm

SCALARS = {
    "owner": r"^(?:owner|agency)\s*:\s*(.+)$",
    "project": r"^project\s*:\s*(.+)$",
    "location": r"^location\s*:\s*(.+)$",
    "bid_due": r"\bbids? due\s*:\s*(.+)$",
    "est_value": r"(?:engineer's estimate|estimated construction cost|estimated value)\s*:\s*(\$[\d,]+)",
    "bid_bond_pct": r"\bbid (?:bond|security)\b[^%]*?(\d+\s*%)",
    "perf_bond_pct": r"\bperformance (?:and payment )?bonds?\b[^%]*?(\d+\s*%)",
    "ld_per_day": r"liquidated damages[^$]*(\$[\d,]+)\s*(?:per|/)\s*(?:calendar )?day",
    "prevailing_wage": r"(.*\bprevailing wage.*)",
    "prebid_mandatory": r"(.*\b(?:pre-?bid|job walk)\b.*)",
}

# Where to look when a fact is missing, so a "missing" finding can still point at the line that
# mentions the topic (for example a bid form that says "bid security per Section 00 21 13").
HINTS = {
    "est_value": r"estimate|budget|construction cost",
    "bid_bond_pct": r"\bbid (?:bond|security)",
    "perf_bond_pct": r"performance",
    "ld_per_day": r"liquidated",
    "location": r"location|county",
    "prevailing_wage": r"prevailing|public works",
}

# CSI section number -> trade, checked in order.
TRADES = [
    (r"^26 5", "lighting"),
    (r"^26", "power"),
    (r"^27 53", "bda_errcs"),
    (r"^27", "low_voltage"),
    (r"^28 1", "access_control"),
    (r"^28 2", "cctv"),
    (r"^28 [34]", "fire_alarm"),
]

SECTION_HEAD = r"^SECTION (\d\d \d\d \d\d)\s*-\s*(.+)$"


def to_number(raw):
    return int(re.sub(r"[^\d]", "", raw))


def to_bool(field, raw):
    s = raw.lower()
    if field == "prevailing_wage":
        return not re.search(r"\bnot (?:subject|required)|\bexempt", s)
    if field == "prebid_mandatory":
        return "mandatory" in s and not re.search(r"not mandatory|non-mandatory", s)
    return s in ("true", "yes")


def normalize(field, raw):
    """Turn the text that was found into a typed value. Shared by the regex and Claude paths."""
    if field in ("est_value", "bid_bond_pct", "perf_bond_pct", "ld_per_day"):
        return to_number(raw)
    if field in ("prevailing_wage", "prebid_mandatory"):
        return to_bool(field, raw)
    return raw.strip().rstrip(".")


def supports(field, raw, quote):
    """Does the quoted line actually say this value? Used to reject unsupported model claims."""
    q = quote.lower()
    if field in ("est_value", "ld_per_day"):
        return str(to_number(raw)) in re.sub(r"[,$\s]", "", q)
    if field in ("bid_bond_pct", "perf_bond_pct"):
        return re.search(rf"\b{to_number(raw)}\s*%", q) is not None
    if field == "prevailing_wage":
        return "prevailing wage" in q and to_bool(field, raw) == to_bool(field, q)
    if field == "prebid_mandatory":
        return re.search(r"pre-?bid|job walk", q) is not None and to_bool(field, raw) == to_bool(field, q)
    return norm(raw.rstrip(".")) in norm(q)


def first(passages, pattern, flags=re.I):
    for pid, text in passages.items():
        m = re.search(pattern, text, flags)
        if m:
            return pid, text, m
    return None


def regex_scalars(passages):
    facts = {}
    for field, pattern in SCALARS.items():
        hit = first(passages, pattern)
        facts[field] = None
        if hit:
            pid, text, m = hit
            facts[field] = {"value": normalize(field, m.group(1)), "cite": {"id": pid, "quote": text}}
    return facts


def structure(passages):
    """Things read from the package's structure: sections, sheets, addenda, licenses, trades."""
    sections, trades, addenda, licenses = {}, [], [], []
    sheets_ref, sections_ref, sheets_given = [], [], {}
    in_index = None
    for pid, text in passages.items():
        doc = pid.split(":")[0]
        cite = {"id": pid, "quote": text}
        head = re.match(SECTION_HEAD, text)
        if head:
            sections[head.group(1)] = cite
            trade = next((t for pat, t in TRADES if re.match(pat, head.group(1))), None)
            if trade:
                trades.append({"value": trade, "section": head.group(1), "cite": cite})
        if re.match(r"^ADDENDUM NO\.?\s*\d+", text, re.I):
            addenda.append(cite)
        if "license" in text.lower() and re.search(r"required|must|shall", text, re.I):
            for code in re.findall(r"\bC-\d+\b", text):
                if not any(code == l["value"] for l in licenses):
                    licenses.append({"value": code, "cite": cite})
        if "DRAWINGS INCLUDED" in text.upper():
            in_index = doc
            continue
        given = re.match(r"^Sheet ([A-Z]{1,2}-\d{3})\b", text)
        if in_index == doc and given:
            sheets_given[given.group(1)] = cite
            continue
        for sheet in re.findall(r"\bSheet ([A-Z]{1,2}-\d{3})\b", text):
            sheets_ref.append({"value": sheet, "cite": cite})
        if not head:
            for sec in re.findall(r"\bSection (\d\d \d\d \d\d)\b", text):
                sections_ref.append({"value": sec, "cite": cite})
    return {
        "trades": trades,
        "licenses_required": licenses,
        "addenda": addenda,
        "sections_provided": sections,
        "sheets_provided": sheets_given,
        "missing_refs": [r for r in sheets_ref if r["value"] not in sheets_given]
        + [r for r in sections_ref if r["value"] not in sections],
    }


def county_of(location):
    if not location:
        return None
    m = re.search(r"([A-Z][a-z]+(?: [A-Z][a-z]+)?) County", location["value"])
    return {"value": m.group(1), "cite": location["cite"]} if m else None


def hints(passages, field, limit=3):
    pattern = HINTS.get(field)
    if not pattern:
        return []
    return [{"id": pid, "quote": t} for pid, t in passages.items() if re.search(pattern, t, re.I)][:limit]


def extract(passages, scalar_extractor=None):
    """scalar_extractor(passages) -> (facts, rejected). Defaults to the regex extractor."""
    if scalar_extractor:
        facts, rejected = scalar_extractor(passages)
    else:
        facts, rejected = regex_scalars(passages), []
    facts["county"] = county_of(facts.get("location"))
    facts.update(structure(passages))
    return facts, rejected

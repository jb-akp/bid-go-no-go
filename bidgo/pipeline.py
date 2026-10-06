import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import yaml

from . import memo
from .extract import extract
from .ingest import ingest
from .rules import evaluate, recommend

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "data/company_profile.yaml"
OPPS = ROOT / "data/opportunities"
OUT = ROOT / "out"
DECISIONS = ("GO", "HOLD", "NO-GO")


def scalar_extractor():
    if os.environ.get("BIDGO_EXTRACTOR") == "claude":
        from .claude_extract import claude_scalars
        return "claude", claude_scalars
    return "rules (regex, offline)", None


def run(package, profile_path=PROFILE, out=OUT):
    package = Path(package)
    profile = yaml.safe_load(Path(profile_path).read_text())
    passages = ingest(package)
    label, fn = scalar_extractor()
    facts, rejected = extract(passages, fn)
    checks = evaluate(facts, profile, passages)
    decision, reasons = recommend(checks)
    result = {
        "name": package.name, "decision": decision, "reasons": reasons, "checks": checks,
        "facts": facts, "rejected": rejected, "extractor": label, "company": profile["company"],
        "documents": len({p.split(":")[0] for p in passages}), "passages": len(passages),
    }
    out = Path(out)
    out.mkdir(exist_ok=True)
    (out / f"{package.name}.md").write_text(memo.render(result))
    (out / f"{package.name}.json").write_text(json.dumps(result, indent=2))
    return result, passages


def approve(name, by, decision, note="", out=OUT):
    """The only step that records a decision. It writes one line to approvals.jsonl and nothing else."""
    out = Path(out)
    decision = decision.upper()
    if decision not in DECISIONS:
        raise SystemExit(f"--decision must be one of {', '.join(DECISIONS)}")
    memo_path, data_path = out / f"{name}.md", out / f"{name}.json"
    if not data_path.exists():
        raise SystemExit(f"No memo for {name}. Run: python -m bidgo run data/opportunities/{name}")
    recommended = json.loads(data_path.read_text())["decision"]
    override = decision != recommended
    if override and not note.strip():
        raise SystemExit(f"Overriding {recommended} to {decision} needs a --note explaining why.")
    entry = {
        "opportunity": name, "recommended": recommended, "decision": decision, "override": override,
        "by": by, "note": note, "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "memo_sha256": hashlib.sha256(memo_path.read_bytes()).hexdigest(),
    }
    with open(out / "approvals.jsonl", "a") as fh:
        fh.write(json.dumps(entry) + "\n")
    return entry

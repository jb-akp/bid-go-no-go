"""Step 6: the bid memo management reads. Every line in it points back at a document line."""

LABELS = [
    ("owner", "Owner"), ("project", "Project"), ("location", "Location"), ("bid_due", "Bid due"),
    ("est_value", "Estimate"), ("bid_bond_pct", "Bid bond"), ("perf_bond_pct", "Performance bond"),
    ("ld_per_day", "Liquidated damages"), ("prevailing_wage", "Prevailing wage"),
    ("prebid_mandatory", "Mandatory pre-bid walk"),
]


def show(field, value):
    if field in ("est_value", "ld_per_day"):
        return f"${value:,}" + ("/day" if field == "ld_per_day" else "")
    if field.endswith("_pct"):
        return f"{value}%"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value)


def src(cite, width=120):
    q = cite["quote"]
    q = q if not width or len(q) <= width else q[: width - 3] + "..."
    return f'`{cite["id"]}` "{q}"'


def render(result):
    f, name = result["facts"], result["name"]
    title = f["project"]["value"] if f["project"] else name
    lines = [
        f"# Bid memo: {title}",
        "",
        f"**Recommendation: {result['decision']}**  ",
        f"Package `{name}`: {result['documents']} documents, {result['passages']} passages. "
        f"Extractor: {result['extractor']}. Profile: {result['company']}.",
        "",
        "## Why",
        "",
    ]
    for i, r in enumerate(result["reasons"], 1):
        lines.append(f"{i}. **{r['check']}**: {r['detail']}")
        lines += [f"   - {src(c, None)}" for c in r["cites"]]
    lines += ["", "## Key facts", "", "| Field | Value | Source |", "|---|---|---|"]
    for field, label in LABELS:
        fact = f.get(field)
        lines.append(f"| {label} | {show(field, fact['value'])} | {src(fact['cite'], 60)} |" if fact
                     else f"| {label} | **not stated** | - |")
    lines.append(f"| Addenda in package | {len(f['addenda'])} | "
                 + (", ".join(f"`{c['id']}`" for c in f["addenda"]) or "-") + " |")
    lines += ["", "## Checks against company profile", "", "| Result | Check | Detail | Profile key | Source |",
              "|---|---|---|---|---|"]
    for c in result["checks"]:
        cites = "<br>".join(f"`{x['id']}`" for x in c["cites"]) or "-"
        lines.append(f"| {c['result']} | {c['check']} | {c['detail']} | `{c['profile_key']}` | {cites} |")
    risks = [c for c in result["checks"] if c["result"] == "WARN"]
    lines += ["", "## Risks for the reviewer", ""]
    lines += [f"- **{c['check']}**: {c['detail']} {src(c['cites'][0], 70)}" for c in risks] or ["- None flagged."]
    lines.append("- Margin (target from `min_margin_pct`) is set by the estimator after takeoff; not checked here.")
    if result["rejected"]:
        lines += ["", "## Rejected model claims (not used)", ""]
        lines += [f"- {r['field']} = {r['value']!r} citing `{r['cite']['id']}`: {r['why']}" for r in result["rejected"]]
    lines += [
        "", "## Approve / Override", "",
        "Nothing has been sent, submitted or committed. A person decides here.", "",
        f"- [ ] Approve {result['decision']}",
        "- [ ] Override to: GO / HOLD / NO-GO (note required)",
        "- Reviewer: ____________  Date: ________  Note: ______________________", "",
        "Record the decision:", "",
        "```",
        f'python -m bidgo approve {name} --by "Your Name" --decision {result["decision"]} --note "..."',
        "```",
        "",
    ]
    return "\n".join(lines)

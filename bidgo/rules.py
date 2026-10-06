"""Steps 3-5: check the facts against the company profile, list risks, recommend GO / HOLD / NO-GO.

All of this is plain code. Each check names the profile key it used and cites the passage(s)
the fact came from. The recommendation is mechanical:
  any FAIL     -> NO-GO  (the reasons are the FAILs)
  any MISSING  -> HOLD   (the reasons are the MISSING items, i.e. what to ask the owner for)
  otherwise    -> GO     (the reasons are the PASSes)
WARN items never change the decision; they go in front of the reviewer as risks.
"""
from .extract import hints


def money(n):
    return f"${n:,.0f}"


def evaluate(facts, profile, passages):
    checks = []

    def add(check, result, key, detail, cites):
        cites = list({c["id"]: c for c in cites}.values())
        checks.append({"check": check, "result": result, "profile_key": key, "detail": detail, "cites": cites})

    def missing(check, key, field, what):
        add(check, "MISSING", key, f"{what} is not stated in the package.", hints(passages, field))

    est, county = facts["est_value"], facts["county"]

    # Service area
    areas = profile["service_area_counties"]
    if county:
        ok = county["value"] in areas
        add("Service area", "PASS" if ok else "FAIL", "service_area_counties",
            f"{county['value']} County is {'inside' if ok else 'outside'} the service area ({', '.join(areas)}).",
            [county["cite"]])
    else:
        missing("Service area", "service_area_counties", "location", "The project county")

    # Licenses
    need = facts["licenses_required"]
    lacking = [l for l in need if l["value"] not in profile["licenses"]]
    if need:
        add("License", "FAIL" if lacking else "PASS", "licenses",
            f"Package names {', '.join(l['value'] for l in need)}; we hold {', '.join(profile['licenses'])}.",
            [l["cite"] for l in need])

    # Size, backlog, bonding (all need the estimate)
    if est:
        v = est["value"]
        size = profile["project_size"]
        ok = size["min_value"] <= v <= size["max_value"]
        add("Project size", "PASS" if ok else "FAIL", "project_size.max_value",
            f"Estimate {money(v)} vs our range {money(size['min_value'])} to {money(size['max_value'])}.", [est["cite"]])
        room = profile["backlog"]["capacity"] - profile["backlog"]["current"]
        add("Backlog capacity", "PASS" if v <= room else "FAIL", "backlog.capacity",
            f"Estimate {money(v)} vs {money(room)} of open capacity "
            f"({money(profile['backlog']['current'])} backlog of {money(profile['backlog']['capacity'])}).", [est["cite"]])
    else:
        for name, key in (("Project size", "project_size.max_value"), ("Backlog capacity", "backlog.capacity")):
            missing(name, key, "est_value", "The engineer's estimate")

    perf = facts["perf_bond_pct"]
    if perf and est:
        bond = est["value"] * perf["value"] / 100
        limit = min(profile["bonding"]["single_project_limit"], profile["bonding"]["aggregate_remaining"])
        add("Performance bond", "PASS" if bond <= limit else "FAIL", "bonding.single_project_limit",
            f"{perf['value']}% of {money(est['value'])} = {money(bond)} vs bonding limit {money(limit)}.",
            [perf["cite"], est["cite"]])
    elif not perf:
        missing("Performance bond", "bonding.single_project_limit", "perf_bond_pct", "The performance bond percentage")

    bid = facts["bid_bond_pct"]
    if bid:
        add("Bid bond", "PASS", "bonding.single_project_limit", f"Bid bond {bid['value']}% stated.", [bid["cite"]])
    else:
        missing("Bid bond", "bonding.single_project_limit", "bid_bond_pct", "The bid bond / bid security amount")

    # Liquidated damages
    ld, cap = facts["ld_per_day"], profile["max_ld_per_day"]
    if ld:
        add("Liquidated damages", "PASS" if ld["value"] <= cap else "FAIL", "max_ld_per_day",
            f"{money(ld['value'])}/day vs our limit {money(cap)}/day.", [ld["cite"]])
    else:
        missing("Liquidated damages", "max_ld_per_day", "ld_per_day", "The liquidated damages rate")

    # Trades: scope we don't self-perform is a risk (needs a sub), not a disqualifier
    for t in facts["trades"]:
        ours = t["value"] in profile["trades"]
        add(f"Scope {t['section']}", "PASS" if ours else "WARN", "trades",
            f"{t['value']} is {'self-performed' if ours else 'NOT self-performed; needs a subcontractor quote'}.",
            [t["cite"]])

    # Prevailing wage
    pw = facts["prevailing_wage"]
    if pw:
        ok = not pw["value"] or profile["prevailing_wage"]["capable"]
        add("Prevailing wage", "PASS" if ok else "FAIL", "prevailing_wage.capable",
            "Prevailing wage applies; we are DIR registered with certified payroll." if pw["value"]
            else "Not a prevailing wage job.", [pw["cite"]])

    # Pre-bid walk
    pb = facts["prebid_mandatory"]
    if pb and pb["value"]:
        add("Pre-bid walk", "WARN", "-", "Mandatory attendance; the bid is rejected if nobody attends.", [pb["cite"]])

    # Documents referenced but not in the package
    refs = {}
    for ref in facts["missing_refs"]:
        refs.setdefault(ref["value"], []).append(ref["cite"])
    for value, cites in refs.items():
        kind = "Section" if " " in value else "Sheet"
        add(f"Missing {kind} {value}", "MISSING", "-",
            f"{kind} {value} is referenced {len(cites)}x but is not in the package.", cites)

    # Watch terms from the profile
    for term, note in profile.get("watch_terms", {}).items():
        for pid, text in passages.items():
            if term in text.lower():
                add(f"Watch: {term}", "WARN", f"watch_terms.{term}", note, [{"id": pid, "quote": text}])
                break

    return checks


def recommend(checks):
    for result, decision in (("FAIL", "NO-GO"), ("MISSING", "HOLD"), ("PASS", "GO")):
        reasons = [c for c in checks if c["result"] == result]
        if reasons:
            return decision, reasons
    return "HOLD", []

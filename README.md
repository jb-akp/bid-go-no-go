# Bid go / no-go review

A small, readable example of how an electrical and low-voltage contractor could review bid opportunities
with software doing the reading and a person making the call. It takes a bid package (invitation email,
spec excerpts, addenda, bid form, schedule, drawing index), splits every document into numbered lines,
pulls out the commercial and technical facts, checks them against the company's own profile (licenses,
bonding, service area, backlog, trades, LD tolerance), lists what's risky or missing, and writes a
GO / HOLD / NO-GO memo for management. Every fact, check and reason points at a document and line
number, so the recommendation can be checked line by line instead of trusted. Nothing is sent or
submitted; a decision is only recorded when a person runs `approve`.

All data in this repo is fictional: the contractor, the three owners, addresses, amounts and bid numbers.

## What this shows

- **Multi-document, multi-step.** ingest -> extract -> rules check -> risks / missing info -> recommendation -> memo -> human approval.
- **Traceable, not an opinion.** Passage ids look like `04-addendum-02.md:5`. Tests confirm every citation resolves to real text.
- **The decision is code, not a model.** Any FAIL is NO-GO, any MISSING is HOLD, otherwise GO. Each check names the profile key it used (`bonding.single_project_limit`, `max_ld_per_day`, ...).
- **HOLD is useful.** It says exactly what to ask the owner for, and which lines prove it's missing.
- **The model can't sneak a claim in.** On the optional Claude path, an answer whose quote isn't on the cited line, or doesn't say the value, is rejected and listed in the memo. A rejected field counts as missing, so it can only push toward HOLD.

## The three sample packages

| Package | Result | Why |
|---|---|---|
| `fremont-library-upgrade` | GO | Alameda County, $1.18M, 100% bond inside the $3M limit, $500/day LDs, all scope self-performed, every referenced sheet present |
| `sjusd-lincoln-errcs` | HOLD | Addendum 2 references Sheet T-201, which isn't in the package; bid security points to Section 00 21 13, also not provided |
| `fresno-jail-security` | NO-GO | Fresno County is outside the service area; $6.75M bond vs $3M limit; $5,000/day LDs vs $1,500 limit; over size and backlog capacity |

## Example memo (the HOLD one)

This is `examples/sjusd-lincoln-errcs.md`, exactly as generated.

## Bid memo: Lincoln High School ERRCS and Low-Voltage Upgrade

**Recommendation: HOLD**  
Package `sjusd-lincoln-errcs`: 6 documents, 42 passages. Extractor: rules (regex, offline). Profile: Bayline Electric & Systems, Inc. (fictional).

### Why

1. **Bid bond**: The bid bond / bid security amount is not stated in the package.
   - `01-invitation-email.txt:15` "Bid documents are on the district bid portal. Bid security requirements are stated in Section 00 21 13."
   - `05-bid-form.md:5` "Bid security: in the amount required by Section 00 21 13, Instructions to Bidders."
2. **Missing Sheet T-201**: Sheet T-201 is referenced 3x but is not in the package.
   - `02-spec-excerpts.md:14` "Provide a Class B bi-directional amplifier (BDA), donor antenna and distributed antenna system to meet CFC 510. Riser and antenna layout per Sheet T-201."
   - `04-addendum-02.md:5` "1. Section 27 53 19: donor antenna relocated to the gym roof. See revised Sheet T-201 (Rev 1)."
   - `04-addendum-02.md:6` "2. Revised Sheet T-201 will be posted to the bid portal under separate cover."
3. **Missing Section 00 21 13**: Section 00 21 13 is referenced 2x but is not in the package.
   - `01-invitation-email.txt:15` "Bid documents are on the district bid portal. Bid security requirements are stated in Section 00 21 13."
   - `05-bid-form.md:5` "Bid security: in the amount required by Section 00 21 13, Instructions to Bidders."

### Key facts

| Field | Value | Source |
|---|---|---|
| Owner | San Jose Unified School District | `01-invitation-email.txt:5` "Owner: San Jose Unified School District" |
| Project | Lincoln High School ERRCS and Low-Voltage Upgrade | `01-invitation-email.txt:6` "Project: Lincoln High School ERRCS and Low-Voltage Upgrade" |
| Location | 555 Dana Ave, San Jose, Santa Clara County, CA | `01-invitation-email.txt:7` "Location: 555 Dana Ave, San Jose, Santa Clara County, CA" |
| Bid due | November 5, 2026 at 11:00 AM PT | `01-invitation-email.txt:9` "Bids due: November 5, 2026 at 11:00 AM PT" |
| Estimate | $840,000 | `01-invitation-email.txt:8` "Estimated construction cost: $840,000" |
| Bid bond | **not stated** | - |
| Performance bond | 100% | `02-spec-excerpts.md:5` "Performance and payment bonds: 100% each of the contract ..." |
| Liquidated damages | $750/day | `02-spec-excerpts.md:4` "Liquidated damages: $750 per calendar day." |
| Prevailing wage | yes | `01-invitation-email.txt:13` "This is a public works project subject to prevailing wage..." |
| Mandatory pre-bid walk | yes | `01-invitation-email.txt:10` "Mandatory pre-bid job walk: October 15, 2026 at 3:30 PM. ..." |
| Addenda in package | 2 | `03-addendum-01.md:1`, `04-addendum-02.md:1` |

### Checks against company profile

| Result | Check | Detail | Profile key | Source |
|---|---|---|---|---|
| PASS | Service area | Santa Clara County is inside the service area (Alameda, Contra Costa, Santa Clara, San Mateo, San Francisco). | `service_area_counties` | `01-invitation-email.txt:7` |
| PASS | License | Package names C-10, C-7; we hold C-10, C-7. | `licenses` | `01-invitation-email.txt:12` |
| PASS | Project size | Estimate $840,000 vs our range $75,000 to $3,500,000. | `project_size.max_value` | `01-invitation-email.txt:8` |
| PASS | Backlog capacity | Estimate $840,000 vs $2,800,000 of open capacity ($6,200,000 backlog of $9,000,000). | `backlog.capacity` | `01-invitation-email.txt:8` |
| PASS | Performance bond | 100% of $840,000 = $840,000 vs bonding limit $3,000,000. | `bonding.single_project_limit` | `02-spec-excerpts.md:5`<br>`01-invitation-email.txt:8` |
| MISSING | Bid bond | The bid bond / bid security amount is not stated in the package. | `bonding.single_project_limit` | `01-invitation-email.txt:15`<br>`05-bid-form.md:5` |
| PASS | Liquidated damages | $750/day vs our limit $1,500/day. | `max_ld_per_day` | `02-spec-excerpts.md:4` |
| PASS | Scope 26 05 19 | power is self-performed. | `trades` | `02-spec-excerpts.md:7` |
| PASS | Scope 27 10 00 | low_voltage is self-performed. | `trades` | `02-spec-excerpts.md:10` |
| PASS | Scope 27 53 19 | bda_errcs is self-performed. | `trades` | `02-spec-excerpts.md:13` |
| PASS | Prevailing wage | Prevailing wage applies; we are DIR registered with certified payroll. | `prevailing_wage.capable` | `01-invitation-email.txt:13` |
| WARN | Pre-bid walk | Mandatory attendance; the bid is rejected if nobody attends. | `-` | `01-invitation-email.txt:10` |
| MISSING | Missing Sheet T-201 | Sheet T-201 is referenced 3x but is not in the package. | `-` | `02-spec-excerpts.md:14`<br>`04-addendum-02.md:5`<br>`04-addendum-02.md:6` |
| MISSING | Missing Section 00 21 13 | Section 00 21 13 is referenced 2x but is not in the package. | `-` | `01-invitation-email.txt:15`<br>`05-bid-form.md:5` |
| WARN | Watch: fcc grol | BDA work needs an FCC GROL holder on the crew. | `watch_terms.fcc grol` | `02-spec-excerpts.md:15` |

### Risks for the reviewer

- **Pre-bid walk**: Mandatory attendance; the bid is rejected if nobody attends. `01-invitation-email.txt:10` "Mandatory pre-bid job walk: October 15, 2026 at 3:30 PM. Bids from ..."
- **Watch: fcc grol**: BDA work needs an FCC GROL holder on the crew. `02-spec-excerpts.md:15` "Contractor shall hold or employ a technician with a current FCC GRO..."
- Margin (target from `min_margin_pct`) is set by the estimator after takeoff; not checked here.

### Approve / Override

Nothing has been sent, submitted or committed. A person decides here.

- [ ] Approve HOLD
- [ ] Override to: GO / HOLD / NO-GO (note required)
- Reviewer: ____________  Date: ________  Note: ______________________

Record the decision:

```
python -m bidgo approve sjusd-lincoln-errcs --by "Your Name" --decision HOLD --note "..."
```

## Run it

Python 3.10+. Offline by default, no API key needed.

```
pip install -r requirements.txt
python -m bidgo run data/opportunities/sjusd-lincoln-errcs   # prints the decision, writes out/<name>.md and .json
python -m bidgo run-all
python -m bidgo approve sjusd-lincoln-errcs --by "Pat Lee" --decision HOLD --note "Asked district for T-201 and the ITB"
python -m pytest -q
```

`approve` appends one line to `out/approvals.jsonl` (who, what, recommended vs chosen, note, time, and a
hash of the memo they approved). Overriding the recommendation requires a `--note`. `examples/` holds
the output of one full run.

## Optional: Claude as the extractor

```
export ANTHROPIC_API_KEY=...
BIDGO_EXTRACTOR=claude python -m bidgo run-all
```

Claude (`claude-sonnet-5`, change with `BIDGO_MODEL`) gets the numbered passages and must return each field
as structured output: value, passage id, exact quote. `bidgo/claude_extract.py` then checks that the passage
exists, the quote is on that line, and the quote states the value. Anything that fails is dropped. Sections,
sheets, addenda, licenses and trades are always read by code.

**The live Claude path has not been run for this repo** (no key used). The tests and `examples/` use the
offline regex extractor; the citation check that guards the Claude path is tested with fake model answers.

## How this would grow

- **Ingest:** watch the estimating inbox and the bid portals (PlanetBids, BidNet, BuildingConnected) and drop each opportunity into its own package folder.
- **PDF parsing:** specs, addenda and bid forms arrive as PDFs. Passage ids become `file:page:line`, and drawing sheet indexes are read from the title blocks.
- **Your real capability sheet:** replace `data/company_profile.yaml` with your actual licenses, surety letter, counties, backlog and the terms you always want flagged.
- **More rules:** days until bid due vs estimating workload, DBE/SBE goals, insurance limits, retention, owner payment history.
- **A review UI:** a queue of memos where an estimator or manager clicks a citation to see the source page, then approves or overrides. Approval is the gate before anything goes to estimating or a bid gets submitted.

## Files

- `bidgo/ingest.py` documents -> numbered passages, and the citation check
- `bidgo/extract.py` regex extractor, structure reader (sections, sheets, addenda, trades), value checks
- `bidgo/claude_extract.py` optional Claude extractor with citation verification
- `bidgo/rules.py` checks against the profile and the GO / HOLD / NO-GO rule
- `bidgo/memo.py` the management memo
- `bidgo/pipeline.py` `run` and `approve`
- `data/` fictional company profile and three bid packages

Built by James Bradford. MIT license.

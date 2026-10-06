# Bid memo: Lincoln High School ERRCS and Low-Voltage Upgrade

**Recommendation: HOLD**  
Package `sjusd-lincoln-errcs`: 6 documents, 42 passages. Extractor: rules (regex, offline). Profile: Bayline Electric & Systems, Inc. (fictional).

## Why

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

## Key facts

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

## Checks against company profile

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

## Risks for the reviewer

- **Pre-bid walk**: Mandatory attendance; the bid is rejected if nobody attends. `01-invitation-email.txt:10` "Mandatory pre-bid job walk: October 15, 2026 at 3:30 PM. Bids from ..."
- **Watch: fcc grol**: BDA work needs an FCC GROL holder on the crew. `02-spec-excerpts.md:15` "Contractor shall hold or employ a technician with a current FCC GRO..."
- Margin (target from `min_margin_pct`) is set by the estimator after takeoff; not checked here.

## Approve / Override

Nothing has been sent, submitted or committed. A person decides here.

- [ ] Approve HOLD
- [ ] Override to: GO / HOLD / NO-GO (note required)
- Reviewer: ____________  Date: ________  Note: ______________________

Record the decision:

```
python -m bidgo approve sjusd-lincoln-errcs --by "Your Name" --decision HOLD --note "..."
```

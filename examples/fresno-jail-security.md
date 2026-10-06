# Bid memo: Main Jail Security Electronics Replacement

**Recommendation: NO-GO**  
Package `fresno-jail-security`: 5 documents, 40 passages. Extractor: rules (regex, offline). Profile: Bayline Electric & Systems, Inc. (fictional).

## Why

1. **Service area**: Fresno County is outside the service area (Alameda, Contra Costa, Santa Clara, San Mateo, San Francisco).
   - `01-invitation-email.txt:7` "Location: 1225 M Street, Fresno, Fresno County, CA"
2. **Project size**: Estimate $6,750,000 vs our range $75,000 to $3,500,000.
   - `01-invitation-email.txt:8` "Engineer's Estimate: $6,750,000"
3. **Backlog capacity**: Estimate $6,750,000 vs $2,800,000 of open capacity ($6,200,000 backlog of $9,000,000).
   - `01-invitation-email.txt:8` "Engineer's Estimate: $6,750,000"
4. **Performance bond**: 100% of $6,750,000 = $6,750,000 vs bonding limit $3,000,000.
   - `02-spec-excerpts.md:5` "Performance bond: 100% of the contract price. Payment bond: 100% of the contract price."
   - `01-invitation-email.txt:8` "Engineer's Estimate: $6,750,000"
5. **Liquidated damages**: $5,000/day vs our limit $1,500/day.
   - `02-spec-excerpts.md:9` "Liquidated damages: $5,000 per calendar day."

## Key facts

| Field | Value | Source |
|---|---|---|
| Owner | County of Fresno, Sheriff-Coroner's Office | `01-invitation-email.txt:5` "Owner: County of Fresno, Sheriff-Coroner's Office" |
| Project | Main Jail Security Electronics Replacement | `01-invitation-email.txt:6` "Project: Main Jail Security Electronics Replacement" |
| Location | 1225 M Street, Fresno, Fresno County, CA | `01-invitation-email.txt:7` "Location: 1225 M Street, Fresno, Fresno County, CA" |
| Bid due | November 19, 2026 at 2:00 PM PT | `01-invitation-email.txt:9` "Bids due: November 19, 2026 at 2:00 PM PT" |
| Estimate | $6,750,000 | `01-invitation-email.txt:8` "Engineer's Estimate: $6,750,000" |
| Bid bond | 10% | `02-spec-excerpts.md:4` "Bid bond: 10% of the bid amount." |
| Performance bond | 100% | `02-spec-excerpts.md:5` "Performance bond: 100% of the contract price. Payment bon..." |
| Liquidated damages | $5,000/day | `02-spec-excerpts.md:9` "Liquidated damages: $5,000 per calendar day." |
| Prevailing wage | yes | `01-invitation-email.txt:13` "Prevailing wage rates apply. This project is subject to a..." |
| Mandatory pre-bid walk | yes | `01-invitation-email.txt:10` "Mandatory pre-bid conference and site walk: October 27, 2..." |
| Addenda in package | 1 | `03-addendum-01.md:1` |

## Checks against company profile

| Result | Check | Detail | Profile key | Source |
|---|---|---|---|---|
| FAIL | Service area | Fresno County is outside the service area (Alameda, Contra Costa, Santa Clara, San Mateo, San Francisco). | `service_area_counties` | `01-invitation-email.txt:7` |
| PASS | License | Package names C-10; we hold C-10, C-7. | `licenses` | `01-invitation-email.txt:12` |
| FAIL | Project size | Estimate $6,750,000 vs our range $75,000 to $3,500,000. | `project_size.max_value` | `01-invitation-email.txt:8` |
| FAIL | Backlog capacity | Estimate $6,750,000 vs $2,800,000 of open capacity ($6,200,000 backlog of $9,000,000). | `backlog.capacity` | `01-invitation-email.txt:8` |
| FAIL | Performance bond | 100% of $6,750,000 = $6,750,000 vs bonding limit $3,000,000. | `bonding.single_project_limit` | `02-spec-excerpts.md:5`<br>`01-invitation-email.txt:8` |
| PASS | Bid bond | Bid bond 10% stated. | `bonding.single_project_limit` | `02-spec-excerpts.md:4` |
| FAIL | Liquidated damages | $5,000/day vs our limit $1,500/day. | `max_ld_per_day` | `02-spec-excerpts.md:9` |
| PASS | Scope 26 24 16 | power is self-performed. | `trades` | `02-spec-excerpts.md:12` |
| PASS | Scope 28 13 00 | access_control is self-performed. | `trades` | `02-spec-excerpts.md:15` |
| PASS | Scope 28 23 00 | cctv is self-performed. | `trades` | `02-spec-excerpts.md:18` |
| WARN | Scope 28 46 00 | fire_alarm is NOT self-performed; needs a subcontractor quote. | `trades` | `02-spec-excerpts.md:21` |
| PASS | Prevailing wage | Prevailing wage applies; we are DIR registered with certified payroll. | `prevailing_wage.capable` | `01-invitation-email.txt:13` |
| WARN | Pre-bid walk | Mandatory attendance; the bid is rejected if nobody attends. | `-` | `01-invitation-email.txt:10` |
| WARN | Watch: project labor agreement | We are not PLA signatory; union hiring hall terms would apply. | `watch_terms.project labor agreement` | `01-invitation-email.txt:13` |
| WARN | Watch: background check | Field crew needs clearance before the job walk and before mobilizing. | `watch_terms.background check` | `01-invitation-email.txt:10` |
| WARN | Watch: phased | Phasing in an occupied building adds supervision and remobilization cost. | `watch_terms.phased` | `02-spec-excerpts.md:10` |

## Risks for the reviewer

- **Scope 28 46 00**: fire_alarm is NOT self-performed; needs a subcontractor quote. `02-spec-excerpts.md:21` "SECTION 28 46 00 - FIRE DETECTION AND ALARM"
- **Pre-bid walk**: Mandatory attendance; the bid is rejected if nobody attends. `01-invitation-email.txt:10` "Mandatory pre-bid conference and site walk: October 27, 2026 at 9:0..."
- **Watch: project labor agreement**: We are not PLA signatory; union hiring hall terms would apply. `01-invitation-email.txt:13` "Prevailing wage rates apply. This project is subject to a Project L..."
- **Watch: background check**: Field crew needs clearance before the job walk and before mobilizing. `01-invitation-email.txt:10` "Mandatory pre-bid conference and site walk: October 27, 2026 at 9:0..."
- **Watch: phased**: Phasing in an occupied building adds supervision and remobilization cost. `02-spec-excerpts.md:10` "Work shall be phased so no more than one housing unit is out of ser..."
- Margin (target from `min_margin_pct`) is set by the estimator after takeoff; not checked here.

## Approve / Override

Nothing has been sent, submitted or committed. A person decides here.

- [ ] Approve NO-GO
- [ ] Override to: GO / HOLD / NO-GO (note required)
- Reviewer: ____________  Date: ________  Note: ______________________

Record the decision:

```
python -m bidgo approve fresno-jail-security --by "Your Name" --decision NO-GO --note "..."
```

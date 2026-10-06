# Bid memo: Main Library Lighting and Security Upgrade

**Recommendation: GO**  
Package `fremont-library-upgrade`: 5 documents, 52 passages. Extractor: rules (regex, offline). Profile: Bayline Electric & Systems, Inc. (fictional).

## Why

1. **Service area**: Alameda County is inside the service area (Alameda, Contra Costa, Santa Clara, San Mateo, San Francisco).
   - `01-invitation-email.txt:11` "Location: 2400 Stevenson Blvd, Fremont, Alameda County, CA"
2. **License**: Package names C-10; we hold C-10, C-7.
   - `01-invitation-email.txt:16` "Bidders must hold a valid California C-10 license at time of bid."
3. **Project size**: Estimate $1,180,000 vs our range $75,000 to $3,500,000.
   - `01-invitation-email.txt:12` "Engineer's Estimate: $1,180,000"
4. **Backlog capacity**: Estimate $1,180,000 vs $2,800,000 of open capacity ($6,200,000 backlog of $9,000,000).
   - `01-invitation-email.txt:12` "Engineer's Estimate: $1,180,000"
5. **Performance bond**: 100% of $1,180,000 = $1,180,000 vs bonding limit $3,000,000.
   - `02-spec-excerpts.md:5` "The successful bidder shall furnish a performance bond of 100% and a payment bond of 100% of the contract price."
   - `01-invitation-email.txt:12` "Engineer's Estimate: $1,180,000"
6. **Bid bond**: Bid bond 10% stated.
   - `02-spec-excerpts.md:4` "Bid security: each bid shall be accompanied by a bid bond of 10% of the total bid amount."
7. **Liquidated damages**: $500/day vs our limit $1,500/day.
   - `02-spec-excerpts.md:9` "Liquidated damages: $500 per calendar day for each day beyond contract time."
8. **Scope 26 05 19**: power is self-performed.
   - `02-spec-excerpts.md:11` "SECTION 26 05 19 - LOW-VOLTAGE ELECTRICAL POWER CONDUCTORS AND CABLES"
9. **Scope 26 51 00**: lighting is self-performed.
   - `02-spec-excerpts.md:14` "SECTION 26 51 00 - INTERIOR LIGHTING"
10. **Scope 28 13 00**: access_control is self-performed.
   - `02-spec-excerpts.md:17` "SECTION 28 13 00 - ACCESS CONTROL"
11. **Scope 28 23 00**: cctv is self-performed.
   - `02-spec-excerpts.md:20` "SECTION 28 23 00 - VIDEO SURVEILLANCE"
12. **Prevailing wage**: Prevailing wage applies; we are DIR registered with certified payroll.
   - `01-invitation-email.txt:17` "This project is subject to California prevailing wage requirements and DIR registration."

## Key facts

| Field | Value | Source |
|---|---|---|
| Owner | City of Fremont, Public Works Department | `01-invitation-email.txt:9` "Owner: City of Fremont, Public Works Department" |
| Project | Main Library Lighting and Security Upgrade | `01-invitation-email.txt:10` "Project: Main Library Lighting and Security Upgrade" |
| Location | 2400 Stevenson Blvd, Fremont, Alameda County, CA | `01-invitation-email.txt:11` "Location: 2400 Stevenson Blvd, Fremont, Alameda County, CA" |
| Bid due | November 12, 2026 at 2:00 PM PT | `01-invitation-email.txt:13` "Bids due: November 12, 2026 at 2:00 PM PT" |
| Estimate | $1,180,000 | `01-invitation-email.txt:12` "Engineer's Estimate: $1,180,000" |
| Bid bond | 10% | `02-spec-excerpts.md:4` "Bid security: each bid shall be accompanied by a bid bond..." |
| Performance bond | 100% | `02-spec-excerpts.md:5` "The successful bidder shall furnish a performance bond of..." |
| Liquidated damages | $500/day | `02-spec-excerpts.md:9` "Liquidated damages: $500 per calendar day for each day be..." |
| Prevailing wage | yes | `01-invitation-email.txt:17` "This project is subject to California prevailing wage req..." |
| Mandatory pre-bid walk | no | `01-invitation-email.txt:14` "Pre-bid walk: October 21, 2026 at 10:00 AM (optional, not..." |
| Addenda in package | 1 | `03-addendum-01.md:1` |

## Checks against company profile

| Result | Check | Detail | Profile key | Source |
|---|---|---|---|---|
| PASS | Service area | Alameda County is inside the service area (Alameda, Contra Costa, Santa Clara, San Mateo, San Francisco). | `service_area_counties` | `01-invitation-email.txt:11` |
| PASS | License | Package names C-10; we hold C-10, C-7. | `licenses` | `01-invitation-email.txt:16` |
| PASS | Project size | Estimate $1,180,000 vs our range $75,000 to $3,500,000. | `project_size.max_value` | `01-invitation-email.txt:12` |
| PASS | Backlog capacity | Estimate $1,180,000 vs $2,800,000 of open capacity ($6,200,000 backlog of $9,000,000). | `backlog.capacity` | `01-invitation-email.txt:12` |
| PASS | Performance bond | 100% of $1,180,000 = $1,180,000 vs bonding limit $3,000,000. | `bonding.single_project_limit` | `02-spec-excerpts.md:5`<br>`01-invitation-email.txt:12` |
| PASS | Bid bond | Bid bond 10% stated. | `bonding.single_project_limit` | `02-spec-excerpts.md:4` |
| PASS | Liquidated damages | $500/day vs our limit $1,500/day. | `max_ld_per_day` | `02-spec-excerpts.md:9` |
| PASS | Scope 26 05 19 | power is self-performed. | `trades` | `02-spec-excerpts.md:11` |
| PASS | Scope 26 51 00 | lighting is self-performed. | `trades` | `02-spec-excerpts.md:14` |
| PASS | Scope 28 13 00 | access_control is self-performed. | `trades` | `02-spec-excerpts.md:17` |
| PASS | Scope 28 23 00 | cctv is self-performed. | `trades` | `02-spec-excerpts.md:20` |
| PASS | Prevailing wage | Prevailing wage applies; we are DIR registered with certified payroll. | `prevailing_wage.capable` | `01-invitation-email.txt:17` |

## Risks for the reviewer

- None flagged.
- Margin (target from `min_margin_pct`) is set by the estimator after takeoff; not checked here.

## Approve / Override

Nothing has been sent, submitted or committed. A person decides here.

- [ ] Approve GO
- [ ] Override to: GO / HOLD / NO-GO (note required)
- Reviewer: ____________  Date: ________  Note: ______________________

Record the decision:

```
python -m bidgo approve fremont-library-upgrade --by "Your Name" --decision GO --note "..."
```

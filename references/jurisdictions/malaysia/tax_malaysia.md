# Malaysian Tax Law — Comprehensive Reference

Authority: **Inland Revenue Board of Malaysia (LHDN / IRB)**
Primary legislation: **Income Tax Act 1967 (ITA 1967)**

---

## Table of Contents
1. [Tax Filing by Entity Type](#tax-filing-by-entity-type)
2. [Company Tax (Form C)](#company-tax-form-c)
3. [Individual/Sole Prop Tax (Form B)](#individual-tax-form-b)
4. [Partnership Tax (Form P)](#partnership-tax-form-p)
5. [PLT/LLP Tax (Form PT)](#plt-tax-form-pt)
6. [Koperasi Tax (Form TF)](#koperasi-tax-form-tf)
7. [Trust Tax (Form TP)](#trust-tax-form-tp)
8. [Capital Allowances (Schedule 3)](#capital-allowances)
9. [Non-Deductible Expenses](#non-deductible-expenses)
10. [Double Deductions & Special Deductions](#double-deductions)
11. [Tax Incentives](#tax-incentives)
12. [Transfer Pricing & Anti-Avoidance](#transfer-pricing)
13. [Withholding Tax](#withholding-tax)
14. [Tax Estimation & Instalments](#tax-estimation)
15. [Penalties & Compliance](#penalties)
16. [Budget 2025/2026 Key Changes](#budget-changes)

---

## Tax Filing by Entity Type {#tax-filing-by-entity-type}

| Entity | Form | Due Date | Basis Period |
|---|---|---|---|
| Sdn Bhd / Bhd | Form C | 7 months after FY end | Financial year |
| Sole Proprietor | Form B | 30 June (e-filing: 15 July) | Calendar year (1 Jan - 31 Dec) |
| Partnership | Form P | 30 June | Calendar year |
| PLT (LLP) | Form PT | 7 months after FY end | Financial year |
| Koperasi | Form TF | 7 months after FY end | Financial year |
| Trust | Form TP | 30 April (e-filing: 15 May) | Calendar year |
| Association/Club | Form TF | 7 months after FY end | Financial year |

---

## Company Tax (Form C) {#company-tax-form-c}

### Tax Rates (YA 2024 onwards)

**Standard rate:** 24%

**SME Rate (qualifying conditions):**
- Paid-up capital ≤ RM2.5 million at beginning of basis period
- Gross income from business ≤ RM50 million
- Not controlled by company with paid-up capital > RM2.5 million (directly or indirectly)

| Chargeable Income | Rate |
|---|---|
| First RM150,000 | 15% |
| RM150,001 — RM600,000 | 17% |
| Above RM600,000 | 24% |

**Non-SME (or disqualified):** flat 24% on all chargeable income.

### Computation Structure

```
Adjusted Income from Business
  Gross income (revenue per accounts)
  Less: Allowable deductions (S33)
  Add back: Non-deductible expenses
  Less: Capital allowances absorbed
  = Statutory Income from Business

Add: Other statutory income (interest, rent, royalties, gains)
Less: Approved donations (S44(6)) — max 10% of aggregate income
= Aggregate Income

Less: Current year losses (if multiple sources)
Less: Brought forward losses (max 10 consecutive YAs from YA 2019)
= Total / Chargeable Income

Tax payable = Chargeable Income × applicable rate(s)
Less: Tax rebates (if any)
Less: S108 set-off (pre-single tier — transitional)
Less: S110 set-off (withholding tax credits)
Less: CP204 instalments paid
= Tax payable / (refundable)
```

### Loss Provisions (Post-YA 2019 Amendment)

- **Current year business loss:** can be set off against ALL income sources in same YA
- **Unabsorbed business loss:** carry forward max 10 consecutive YAs (S44(5F))
- **Unabsorbed capital allowances:** carry forward indefinitely (no time limit)
- **Pre-commencement expenses:** S33(1)(e) — deductible if incurred within 3 years before commencement
- **Group relief:** S44A — 70% of adjusted loss can be surrendered to related company (same group, 70%+ ownership)

---

## Individual Tax (Form B) {#individual-tax-form-b}

### Progressive Tax Rates (YA 2024 onwards — Resident)

| Chargeable Income (RM) | Rate | Cumulative Tax (RM) |
|---|---|---|
| 0 — 5,000 | 0% | 0 |
| 5,001 — 20,000 | 1% | 150 |
| 20,001 — 35,000 | 3% | 600 |
| 35,001 — 50,000 | 6% | 1,500 |
| 50,001 — 70,000 | 11% | 3,700 |
| 70,001 — 100,000 | 19% | 9,400 |
| 100,001 — 400,000 | 25% | 84,400 |
| 400,001 — 600,000 | 26% | 136,400 |
| 600,001 — 2,000,000 | 28% | 528,400 |
| Above 2,000,000 | 30% | — |

**Non-resident:** flat 30% (no personal reliefs, no progressive rates)

### Sole Proprietor Computation

```
Business Income (per accounts, accrual basis per S21A)
  Less: Allowable business expenses (S33)
  Add back: Non-deductible / private expenses
  Less: Capital allowances
  = Adjusted Business Income

Add: Employment income (if any)
Add: Other income (interest, rent, royalty, dividends)
= Aggregate Income

Less: Approved donations (S44(6))
Less: Current year / b/f losses
= Total Income

Less: Personal reliefs (S46-S49)
= Chargeable Income

Tax on chargeable income (progressive rates)
Less: Tax rebates
Less: S110 credits
Less: CP500 instalments
= Tax payable / (refundable)
```

### Key Personal Reliefs (S46-S49) — YA 2024

| Relief | Amount (RM) |
|---|---|
| Self | 9,000 |
| Disabled self (additional) | 6,000 |
| Spouse (if no separate assessment) | 4,000 |
| Child (under 18) | 2,000 per child |
| Child (18+ in full-time education) | 8,000 per child |
| Child (disabled) | 6,000 + 8,000 if studying |
| Medical expenses (parents) | Up to 8,000 |
| Medical expenses (self/spouse/child — serious disease) | Up to 10,000 |
| EPF/approved scheme | Up to 4,000 |
| Life insurance / takaful | Up to 3,000 |
| Education expenses (self — Masters/PhD, professional) | Up to 7,000 |
| Lifestyle (books, internet, computer, sport) | Up to 2,500 |
| SSPN (net deposit) | Up to 8,000 |
| Private retirement scheme (PRS) | Up to 3,000 |
| Domestic travel | Up to 1,000 |
| EV charging facilities | Up to 2,500 |

---

## Partnership Tax (Form P) {#partnership-tax-form-p}

- Partnership itself is NOT a taxpaying entity — it files Form P (declaration)
- Profit is allocated to partners per profit-sharing agreement
- Each partner includes their share in personal Form B/BE
- Partnership must still compute adjusted income at partnership level
- Capital allowances claimed at partnership level, allocated to partners
- Partners' salary and interest on capital are appropriations (not deductible from partnership income for tax)

---

## PLT Tax (Form PT) {#plt-tax-form-pt}

- PLT is taxed as a body corporate (like Sdn Bhd)
- Standard rate: 24%
- SME rate available if qualifying conditions met (same as company)
- Files Form PT (7 months after FY end)
- Capital allowances, loss provisions same as companies
- Partners' remuneration: deductible if arm's length (unlike traditional partnership)

---

## Koperasi Tax (Form TF) {#koperasi-tax-form-tf}

| Chargeable Income (RM) | Rate |
|---|---|
| First 30,000 | 0% |
| 30,001 — 60,000 | 5% |
| 60,001 — 100,000 | 10% |
| 100,001 — 150,000 | 15% |
| 150,001 — 250,000 | 18% |
| 250,001 — 500,000 | 20% |
| 500,001 — 750,000 | 22% |
| Above 750,000 | 24% |

- Statutory reserve deduction not deductible for tax
- Dividends to members: not deductible
- Members' patronage rebate: deductible (S65A)
- Exempt cooperatives: Koperasi with members' funds < RM750,000 (income from source other than dividend)

---

## Trust Tax (Form TP) {#trust-tax-form-tp}

- **Resident trust:** income taxed at 24% (rate applicable to body of persons)
- **Non-resident trust:** 30%
- Income distributed to beneficiaries: taxed in beneficiaries' hands (trust gets deduction)
- Undistributed income: taxed in the trust at 24%
- Trustee has duty to file Form TP
- Capital gains: not taxable (except RPGT on real property)

---

## Capital Allowances (Schedule 3 ITA 1967) {#capital-allowances}

### Rates by Asset Class

| Asset Class | Initial Allowance (IA) | Annual Allowance (AA) |
|---|---|---|
| General plant & machinery | 20% | 14% |
| Heavy machinery | 20% | 20% |
| Motor vehicle (cost ≤ RM100,000) | 20% | 20% |
| Motor vehicle (cost ≤ RM200,000, conditions met) | 20% | 20% |
| Motor vehicle (EV, cost ≤ RM300,000) | 20% | 20% |
| Computer & IT equipment | 20% | 20% |
| Office equipment, furniture & fittings | 20% | 10% |
| Industrial building (permanent) | 10% | 3% |
| Building: approved R&D | 50% | - |
| Plantation (oil palm, rubber etc.) | 10%-50% | varies |
| Small value asset (< RM2,000 per item) | 100% | - |
| ICT equipment (accelerated — if qualifying) | 20% | 40% |

### Motor Vehicle Cost Limits

| Condition | Maximum QE |
|---|---|
| New vehicle, on-the-road price | RM100,000 |
| New vehicle, on-the-road price (purchased new, not previously used) | RM200,000 (if conditions in Para 2A Sch 3 met — one vehicle per company exceeding RM100k) |
| Electric vehicle (EV) | RM300,000 (YA 2022-2025) |
| Used vehicle / second-hand | Actual cost or RM100,000 (whichever lower) |

### Small Value Assets (< RM2,000)

- 100% capital allowance in year of acquisition
- Per-item cost must be < RM2,000
- Aggregate limit: RM20,000 per YA (excess → normal IA+AA rates)
- No aggregate limit for SMEs (Income Tax (Deduction for Depreciation of Small Value Assets) Rules 2021)

### Computation Format

```
Qualifying Expenditure (QE) = cost of asset for CA purposes
  Year 1: IA (20% of QE) + AA (rate% of QE) — pro-rated if not full year
  Year 2+: AA only (rate% of QE)
  Continue until fully written down (residual expenditure = 0)

Residual Expenditure = QE - IA - cumulative AA claimed
Balancing Allowance = RE - disposal proceeds (if disposal < RE)
Balancing Charge = disposal proceeds - RE (if disposal > RE, max = total CA claimed)
```

### Key Rules

- IA claimed only ONCE (year asset first used for business)
- AA claimed every year asset is in use for business at end of basis period
- If asset not in use at year end: no AA for that year
- Hire purchase: CA claimed on full cost (not just payments made), IA in year asset first used
- Leased assets: lessee cannot claim CA (lessor claims). Exception: finance lease treated as purchase by lessee for CA purposes if qualifying.

---

## Non-Deductible Expenses {#non-deductible-expenses}

### Specifically Non-Deductible (S39)

| Expense | ITA Reference | Notes |
|---|---|---|
| Domestic/private expenses | S39(1)(a) | Personal expenses of proprietor/partner/director |
| Capital expenditure | S39(1)(b) | Unless specifically allowed (CA, qualifying building) |
| Depreciation (accounting) | S39(1)(b) | Replaced by capital allowances for tax |
| Non-business expenses | S39(1)(c) | Not wholly and exclusively for business |
| Unapproved donations | S39(1)(d) | Only S44(6) approved institutions deductible |
| Tax penalties & fines | S39(1)(f) | LHDN penalties, summons, court fines |
| Provisions (general) | S39(1)(c) | Only specific provisions may qualify |
| Entertainment (general) | S39(1)(l) | Exception: staff entertainment (100%), promotional samples, food/drink for customers |
| Leave passage (excess) | — | Only RM3,000 domestic, one overseas per year |

### Partially Deductible

| Expense | Deductible Portion |
|---|---|
| Entertainment (promotional) | 50% |
| Entertainment (staff) | 100% |
| Motor vehicle (> cost cap) | Only CA on capped amount |
| Pre-commencement expenses | If within 3 years before commencement |
| Interest (thin capitalisation) | Subject to earnings stripping rule |
| Rental of non-business asset | 0% |

### Specifically Deductible (Even Though Capital Nature)

| Expense | ITA Reference |
|---|---|
| Secretarial & tax filing fees | S33(1)(e) |
| Incorporation expenses (first RM25,000) | S33(1)(a) |
| Audit fees | S33(1)(e) |
| Renovation/refurbishment (up to RM300,000 per cycle) | PU(A) 382/2020 |
| Recruitment advertising | S33(1)(d) |
| Training expenses (approved courses) | S33(1)(d) |

---

## Double Deductions & Special Deductions {#double-deductions}

### Double Deductions (200% total deduction)

| Item | Legislation/Rules |
|---|---|
| Export market development: advertising, trade fairs, export credit insurance | ITA S33, PU(A) |
| R&D expenditure (approved by MOSTI) | S34A |
| Training (approved by HRD Corp / PSMB) | S34(6)(n) |
| Employment of disabled persons | PU(A) 73/2021 |
| Sponsorship of arts/cultural activities (approved) | PU(A) |
| Approved green technology expenditure | PU(A) (selected items) |
| Wages for senior citizens (60+ years, salary ≤ RM4,000/month) | S34(6)(ea) |
| Internship structured programme (approved) | S34(6)(eb) |

### Single Special Deductions (100% but not normally deductible)

| Item | Legislation |
|---|---|
| Zakat perniagaan | S44(11A) — deduction up to 2.5% of aggregate income |
| Approved donations (cash/in-kind) | S44(6) — 10% of aggregate income |
| Environmental protection expenditure | PU(A) 172/2020 |
| Scholarship to Malaysian students | S34(6)(i) |

---

## Tax Incentives {#tax-incentives}

### Pioneer Status (PS) — Income Tax (Exemption) Orders

- **What:** 70-100% of statutory income exempt from tax for 5-10 years
- **Who:** Manufacturing, agriculture, tourism, selected services, high-tech, strategic industries
- **Application:** MIDA (Malaysian Investment Development Authority)
- **Computation:** Only 30% (or 0%) of statutory income taxable during pioneer period. Unabsorbed CA and losses accumulated during pioneer period carried forward.
- **Common sectors:** promoted products/activities under Promotion of Investments Act 1986

### Investment Tax Allowance (ITA) — Schedule 7B

- **What:** 60-100% of qualifying capital expenditure as allowance against 70-100% of statutory income
- **Period:** 5-10 years from first qualifying expenditure
- **Alternative to PS** — company chooses one or the other
- **QE:** capital expenditure on plant, machinery, building used for promoted activity
- **Carry forward:** unutilised ITA can be carried forward indefinitely

### Reinvestment Allowance (RA) — Schedule 7A

- **What:** 60% of qualifying capital expenditure, set off against 70% of statutory income
- **Who:** Manufacturing and agriculture companies that have operated ≥ 36 months, reinvesting in same business
- **Period:** 15 consecutive YAs from first RA claim
- **QE:** expenditure on factory, plant & machinery, for purposes of expansion, modernisation, automation, diversification
- **Key restriction:** must be reinvestment in SAME qualifying project/activity

### MSC Malaysia Status

- Tax exemption: 100% of statutory income for 5-10 years (equivalent to Pioneer Status)
- OR Investment Tax Allowance: 100% of QE for 5-10 years
- Eligible: ICT, creative multimedia, shared services, GBS companies
- Must locate in MSC-designated zones (or approved)
- Multimedia super corridor incentives extended to broader digital economy

### Green Technology Incentives

- **Green Investment Tax Allowance (GITA):** 100% of qualifying green technology asset expenditure (set off against 70% of statutory income)
- **Green Income Tax Exemption (GITE):** 70% of statutory income exempt for qualifying green service providers
- **Period:** up to 5 years
- **Qualifying:** certified by Malaysian Green Technology and Climate Change Corporation (MGTC)

### Automation & Industry 4.0

- **Automation Capital Allowance:** first RM4 million of automation equipment (200% AA in first year for qualifying sectors)
- **Industry4WRD:** additional incentives for smart manufacturing transformation

### Principal Hub

- **Reduced tax rate:** 0%, 5%, or 10% on qualifying income for 5+5 years
- **Who:** companies managing, controlling, and supporting regional operations
- **Conditions:** minimum annual operating expenditure, high-value jobs, Treasury management

---

## Transfer Pricing & Anti-Avoidance {#transfer-pricing}

### Transfer Pricing (S140A)

- Applies to transactions between associated persons (related parties, including cross-border)
- Arm's length principle: transactions must be at market value
- DGIR can make adjustments if prices are not arm's length
- **Documentation requirements:** Transfer Pricing Documentation (TPD) mandatory if:
  - Gross income > RM25 million, AND
  - Total related party transactions > RM15 million, OR
  - Financial assistance > RM50 million
- Methods: CUP, Resale Minus, Cost Plus, TNMM, Profit Split
- **Advance Pricing Arrangement (APA):** available bilateral/unilateral — provides certainty for 3-5 years

### Earnings Stripping Rules (S140C) — Replaced Thin Capitalisation

- **Effective:** YA 2019 onwards
- **What:** limits deduction of net interest expense to related party borrowings
- **Threshold:** net interest expense from related-party financial assistance > RM500,000
- **Limit:** max deductible = 20% of tax-EBITDA (from YA 2024)
- **Carry forward:** denied interest can be carried forward (indefinitely, subject to same limit in future years)
- **Exemption:** financial institutions, special purpose vehicles for infrastructure

### General Anti-Avoidance (S140)

- DGIR may disregard any arrangement that has the effect of altering the incidence of tax
- Applies where: arrangement has no bona fide commercial purpose other than tax benefit
- Power to: disregard arrangement, recharacterise, attribute income/gains differently
- Very broad — applies to all schemes with sole/main purpose of obtaining tax benefit

### S140B — Controlled Transactions (Services)

- Services between associated persons must be genuine and at arm's length
- Must demonstrate: service actually rendered, benefit received, no duplication, arm's length charge
- Shareholder activities, duplicative services, and incidental benefits NOT deductible

---

## Withholding Tax {#withholding-tax}

### Key WHT Rates

| Payment Type | Rate | ITA Section | Notes |
|---|---|---|---|
| Interest (non-resident) | 15% | S109 | May be reduced by DTA |
| Royalty (non-resident) | 10% | S109 | May be reduced by DTA |
| Technical/management fees (non-resident) | 10% | S109B | Contract payment — must withhold |
| Rental of moveable property (non-resident) | 10% | S109 | Machinery, equipment |
| Public entertainer | 15% | S109A | |
| Non-resident contractor (building operations) | 10% + 3% | S107A | 10% on contract payment + 3% employee portion |
| Real property gains (non-resident) | Varies | RPGTA | 2% retention by acquirer for RPGT |

### Obligations

- Payer must withhold and remit to LHDN within **one month** of payment/crediting
- Late payment: 10% penalty (S109(7))
- Non-compliance: payer denied deduction for the expense (S39(1)(j))
- DTA countries: may have reduced rates (check specific treaty)

---

## Tax Estimation & Instalments {#tax-estimation}

### Companies (CP204)

- Estimate tax payable for following YA before start of basis period
- Pay in 12 monthly instalments (begin month 2 of basis period)
- Revision: allowed in 6th and 9th month
- Penalty: if actual tax exceeds estimate by > 30% → penalty on shortfall (10%)
- New companies: exempt from CP204 for first 2 YAs

### Individuals / Sole Prop (CP500)

- LHDN issues CP500 notice with instalment amounts (based on prior year)
- Pay in 6 bi-monthly instalments (begin March)
- If new business: no CP500 issued, pay balance with return
- Under-estimation not penalised as heavily as companies (no 30% threshold)

---

## Penalties & Compliance {#penalties}

| Offence | Penalty |
|---|---|
| Late filing (S112(3)) | Fine RM200 - RM20,000, or imprisonment up to 6 months, or both |
| Incorrect return (S113(1)) | Fine RM1,000 - RM10,000 + penalty equal to tax undercharged |
| Willful evasion (S114) | Fine RM1,000 - RM20,000, or imprisonment up to 3 years, or both + penalty 300% of tax |
| Failure to keep records (S119A) | Fine RM300 - RM10,000, or imprisonment up to 1 year |
| Late payment (S103(3)) | 10% increase on unpaid balance |
| CP204 under-estimation (>30%) | 10% on difference between actual and estimated |

**Record retention:** minimum 7 years from end of YA (S82A)

---

## Budget 2025/2026 Key Changes {#budget-changes}

### YA 2024/2025 Changes (As Announced)

| Change | Detail |
|---|---|
| SME rate restructured | 15% (first RM150k), 17% (RM150k-RM600k), 24% (above) |
| Capital gains tax on shares | 10% on gains from disposal of unlisted shares (effective 1 Mar 2024) |
| Global minimum tax (GMT/Pillar 2) | 15% minimum for MNEs with revenue > EUR750m (from 2025) |
| E-invoicing Phase 1 | Revenue > RM100m (from 1 Aug 2024) |
| E-invoicing Phase 2 | Revenue > RM25m (from 1 Jan 2025) |
| E-invoicing Phase 3 | All taxpayers (from 1 Jul 2025) |
| Individual tax rate (top bracket) | 30% on income > RM2m |
| EV capital allowance | Extended to YA 2027, cost limit RM300k |
| Luxury goods tax | 5-10% on selected items > threshold |

### Items to Monitor (Subject to Gazette)

- Earnings stripping rule tightening (20% threshold from YA 2024)
- Transfer pricing documentation threshold changes
- Additional GITA/GITE green incentives
- R&D tax incentives restructuring
- Extended loss carry-forward for specific sectors

---

## Tax Computation Templates

### Company (Form C) — Standard Layout

```
                                                    RM          RM
ADJUSTED INCOME FROM BUSINESS
Net profit per accounts                                     XXX
Add: Non-deductible expenses
  Depreciation                              XXX
  Entertainment (non-staff)                 XXX
  Penalties & fines                         XXX
  Donations (unapproved)                    XXX
  Private expenses                          XXX
  General provisions                        XXX
                                                            XXX
                                                          -----
                                                            XXX
Less: Non-taxable income
  Interest income (taxed separately)        XXX
  Exempt income                             XXX
                                                           (XXX)
                                                          -----
Adjusted Income from Business                               XXX

Less: Capital Allowances
  Balance b/f                               XXX
  Current year IA                           XXX
  Current year AA                           XXX
  Less: Disposal / balancing charge        (XXX)
  Available                                 XXX
  Absorbed (limited to adjusted income)    (XXX)
  Balance c/f                               XXX
                                                           (XXX)
                                                          -----
Statutory Income from Business                              XXX

Add: Other Statutory Income
  Interest income                           XXX
  Rental income                             XXX
                                                            XXX
                                                          -----
Aggregate Income                                            XXX

Less: Approved donation (S44(6)) [max 10%]                 (XXX)
Less: Current year loss from other source                  (XXX)
                                                          -----
Total Income                                                XXX

Less: Unabsorbed losses b/f                                (XXX)
                                                          -----
Chargeable Income                                           XXX
                                                          =====

TAX COMPUTATION
  First RM150,000 @ 15% (SME)                               XXX
  Next RM450,000 @ 17% (SME)                                XXX
  Balance @ 24%                                             XXX
                                                          -----
Tax Charged                                                 XXX
Less: S110 set-off                                         (XXX)
Less: CP204 instalments paid                               (XXX)
                                                          -----
Tax Payable / (Refundable)                                  XXX
                                                          =====
```

### Capital Allowance Schedule

```
Asset | QE | IA | AA (Yr1) | AA (Yr2) | ... | Total CA | RE | BA/BC
```

Always show: brought forward RE from prior year, current year additions (with acquisition date for pro-rating IA+AA), disposals (with balancing allowance/charge computation).

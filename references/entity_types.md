<!-- Compatibility shim: canonical pack lives in references/jurisdictions/malaysia/. Keep in sync when editing. -->

> **Workflow summary — not official standards/tax text.** Verify rates and requirements against MASB / LHDN / MIA.

# Entity Types — Framework Selection & Requirements

## Quick Selection Guide

```
Is the entity publicly listed on Bursa Malaysia?
├── YES → MFRS (= IFRS). File Form C. Read references/mfrs.md
└── NO
    ├── Is it a company (Sdn Bhd)?
    │   └── YES → MPERS. File Form C. Read references/mpers.md
    ├── Is it a PLT / LLP?
    │   └── YES → MPERS. File Form PT. Read references/mpers.md
    ├── Is it a sole proprietor?
    │   └── YES → Accrual basis (S21A ITA 1967). File Form B.
    ├── Is it a partnership?
    │   └── YES → Accrual basis (S21A ITA 1967). File Form P + individual B/BE.
    ├── Is it a Koperasi?
    │   └── YES → MCA Standards. File Form TF.
    ├── Is it a Society / Foundation / Association?
    │   └── YES → Applicable framework (usually cash/accrual hybrid). File Form TF.
    └── Is it a Trust?
        └── YES → MFRS or MPERS (depends on trust deed). File Form TP.
```

---

## 1. Berhad (Bhd) — Public Listed Company

**Registration:** Registered under Companies Act 2016, listed on Bursa Malaysia
**Regulator:** SC (Securities Commission), Bursa Malaysia, SSM, LHDN
**Framework:** MFRS (mandatory, no exemption)
**Tax:** Form C, 24% flat rate (no SME rate for listed companies)

**Key requirements:**
- Full MFRS compliance (all standards)
- Quarterly/annual reporting to Bursa
- Audit mandatory (by MOF-approved auditor)
- EPS disclosure required (MFRS 133)
- Segment reporting required (MFRS 8)
- Cash flow statement mandatory (indirect or direct)
- Related party disclosure (MFRS 124) — extensive
- Directors' responsibility statement
- Corporate governance statement

**Financial Statements (minimum):**
1. Statement of Financial Position
2. Statement of Profit or Loss and OCI
3. Statement of Changes in Equity
4. Statement of Cash Flows
5. Notes (extensive)

**COA considerations:**
- Use full COA with segment coding if multi-segment
- Investment property may use fair value model
- Financial instruments classified per MFRS 9
- Share capital: par value abolished under CA 2016 (use "share capital" not "paid-up capital")

---

## 2. Sdn Bhd — Private Limited Company

**Registration:** SSM (Companies Act 2016), max 50 members
**Regulator:** SSM, LHDN
**Framework:** MPERS (or MFRS if voluntary adoption)
**Tax:** Form C, SME rate if qualifying (15%/17%/24%), else 24% flat

**Key requirements:**
- MPERS Section 3 compliance
- Audit: required unless qualifying for audit exemption (revenue < RM500k, total assets < RM500k, employees < 5 — rarely used in practice)
- Directors' report
- Financial statements lodged with SSM annually
- AGM within 6 months of FY end (or by written resolution for private company)

**Financial Statements (minimum):**
1. Statement of Financial Position
2. Statement of Comprehensive Income (or Income Statement + OCI)
3. Statement of Changes in Equity
4. Statement of Cash Flows (unless small entity exemption)
5. Notes

**COA:** Use `coa_templates/coa_sdn_bhd.json`

---

## 3. PLT / LLP — Limited Liability Partnership

**Registration:** SSM under Limited Liability Partnerships Act 2012
**Regulator:** SSM, LHDN
**Framework:** MPERS (same as Sdn Bhd)
**Tax:** Form PT, taxed as body corporate (same rates as company, SME rate available)

**Key requirements:**
- Minimum 2 partners (can be individuals or bodies corporate)
- Partners' liability limited to agreed contribution
- Must have a compliance officer
- Annual declaration to SSM
- Accounts to be kept (not required to lodge with SSM unless audited)
- Audit: not mandatory unless partnership agreement requires it

**Financial Statements:**
Same as Sdn Bhd under MPERS, but equity section shows:
- Partners' capital contributions (equivalent to share capital)
- Partners' current accounts
- Profit appropriation

**COA considerations:**
- 3000: Partners' Capital Account (not Share Capital)
- 3500: Partners' Current Account (one sub-account per partner)
- 3400: Drawings (if applicable)
- Partners' remuneration is a business expense (deductible for tax — unlike traditional partnership)

**Key difference from traditional partnership:**
- PLT IS a separate legal entity (like Sdn Bhd)
- PLT IS taxed as a body corporate (24% / SME rates)
- PLT partners' remuneration IS deductible (if arm's length)
- Traditional partnership is NOT a legal entity and NOT a taxpayer

---

## 4. Sole Proprietor

**Registration:** SSM (Registration of Businesses Act 1956)
**Regulator:** SSM, LHDN
**Framework:** Accrual basis per S21A ITA 1967 (no specific accounting standard mandated, but good practice follows MPERS principles)
**Tax:** Form B (individual return with business income)

**Key requirements:**
- No separate legal entity — owner IS the business
- No mandatory audit
- Must maintain proper records (S82 ITA — 7 year retention)
- Accrual basis mandatory for tax purposes (S21A)
- Business income assessed together with other personal income

**Financial Statements (for management/lending purposes):**
1. Income Statement (P&L)
2. Balance Sheet (Statement of Financial Position)
3. Notes (if material)

**COA:** Use `coa_templates/coa_sole_prop.json`

**Equity section:**
- 3000: Capital Account (owner's equity — contributions + retained profit)
- 3400: Drawings (personal withdrawals — reduces capital)
- No share capital, no retained earnings (owner's equity is single account rolled forward)

**Special considerations:**
- Personal expenses paid from business account → Drawings (not expense)
- Business assets used personally → apportion (e.g., motor vehicle 70% business, 30% private)
- Capital contribution by owner → CR 3000, DR 1000 Bank
- Zakat perniagaan: deductible up to 2.5% of aggregate income

---

## 5. Partnership (Perkongsian)

**Registration:** SSM (Registration of Businesses Act 1956)
**Regulator:** SSM, LHDN
**Framework:** Accrual basis per S21A ITA 1967
**Tax:** Form P (partnership declaration) + individual Form B/BE for each partner

**Key requirements:**
- NOT a separate legal entity
- NOT a taxpayer (partnership computes income, but partners are taxed individually)
- Min 2, max 20 partners (unless professional partnership)
- Joint and several liability (unless LLP)
- Must have partnership agreement (or Partnership Act 1961 defaults apply)
- Must maintain accounts on accrual basis

**Tax treatment:**
- Adjusted income computed at partnership level (Form P)
- Capital allowances computed at partnership level
- Divisible income allocated to partners per profit-sharing ratio
- Each partner declares their share in individual Form B/BE
- Partners' salary and interest on capital are APPROPRIATIONS (not deductible for partnership)
- Partners' drawings are NOT expenses

**Financial Statements:**
1. Income Statement
2. Profit Appropriation Account (shows allocation to each partner)
3. Partners' Current Accounts (individual running balances)
4. Balance Sheet
5. Notes

**COA:** Use `coa_templates/coa_partnership.json`

**Equity section:**
- 3000: Partners' Capital Account (one per partner — fixed contributions)
- 3500: Partners' Current Account (one per partner — running balance of salary, interest, profit share, drawings)
- 3400: Partners' Drawings (one per partner)

**Profit appropriation format:**
```
Net Profit for the Year                             RM XXX
Appropriation:
  Partners' Salary
    Partner A                          RM XXX
    Partner B                          RM XXX
  Interest on Capital
    Partner A                          RM XXX
    Partner B                          RM XXX
                                                   (RM XXX)
                                                   --------
Residual Profit                                     RM XXX
  Shared in ratio [X:Y]:
    Partner A                          RM XXX
    Partner B                          RM XXX
                                                   (RM XXX)
                                                   --------
                                                    RM NIL
```

---

## 6. Koperasi (Cooperative)

**Registration:** Suruhanjaya Koperasi Malaysia (SKM) under Cooperative Societies Act 1993
**Regulator:** SKM, LHDN
**Framework:** Malaysian Cooperative Accounting Standards (MCA Standards) — simplified accrual framework
**Tax:** Form TF (progressive rates 0%-24%)

**Key requirements:**
- At least 100 members (primary society) or 2 registered societies (secondary)
- Governed by Board of Directors + ALK (Jawatankuasa Audit)
- Annual audit mandatory (by SKM-approved auditor or Jabatan Audit Negara)
- Annual General Meeting (AGM) mandatory
- Statutory reserve: min 12% of net surplus to reserve fund
- Specific allocations: education fund (min 2%), development fund, etc.

**Financial Statements (MCA Standards):**
1. Statement of Receipts and Payments (or Comprehensive Income)
2. Statement of Financial Position
3. Statement of Changes in Members' Funds
4. Notes

**Tax treatment (special provisions):**
- Progressive rates (0% on first RM30k, up to 24%)
- Members' patronage rebate: deductible (S65A)
- Statutory reserve: NOT deductible
- Dividends to members: NOT deductible
- Exempt if members' funds < RM750,000 (on income other than dividends)

**COA considerations:**
- Share capital = Members' shares + subscription fees
- Statutory Reserve Fund (cannot be distributed)
- Education Fund (min 2% of net surplus)
- Members' deposits (if applicable — savings cooperative)
- Members' loans receivable (credit cooperative)

---

## 7. Society / Foundation / Association

**Registration:** Registry of Societies (ROS) under Societies Act 1966, or Companies Commission (MCCM) under Trustees (Incorporation) Act 1952
**Regulator:** ROS/MCCM, LHDN
**Framework:** No mandatory standard; best practice is accrual basis with clear income/expenditure tracking
**Tax:** Form TF, taxed as body of persons at 24% on non-exempt income

**Key requirements:**
- Must have constitution/rules
- Annual accounts presented to AGM
- Audit: mandatory if annual income/expenditure exceeds threshold set by ROS
- Separate funds (general fund, building fund, activity funds) must be tracked

**Financial Statements:**
1. Income and Expenditure Account (not P&L — no "profit")
2. Statement of Financial Position
3. Notes
4. Receipts & Payments Account (some societies still use cash basis supplement)

**Tax treatment:**
- Income from investments, rent, business activities: taxable at 24%
- Membership fees: generally not income (capital contributions to society)
- Donations received: not taxable (unless regular trading income disguised as donation)
- Approved institutions (S44(6)): may issue tax-exempt receipts to donors
- Activities consistent with objectives: may be exempt under S13(1)(a) gazette orders

**COA considerations:**
- No equity/capital in traditional sense
- Accumulated Fund = retained surplus
- Specific funds must be shown separately (restricted vs unrestricted)
- Subscription/membership fees: if recurring annual = income; if one-time joining = equity-like
- Donations received: other income (or restricted fund if earmarked)

---

## 8. Trust (Amanah)

**Registration:** Varies — unit trusts (SC), charitable trusts (ROS/Commissioner of Charities), private trusts (trust deed)
**Regulator:** SC (unit trusts), LHDN, specific trust legislation
**Framework:** MFRS (unit trusts/public trusts) or MPERS (private trusts) depending on nature
**Tax:** Form TP, taxed at 24% on undistributed income

**Key requirements:**
- Created by trust deed
- Trustee holds assets for beneficiaries
- Annual accounts mandatory
- Audit: mandatory for unit trusts and public trusts
- Distributions to beneficiaries: documented and approved by trustee

**Tax treatment:**
- Income of trust: taxed at 24% (body of persons rate)
- Distributed income: taxed in beneficiary's hands, trust gets deduction
- Undistributed income: taxed in the trust
- Capital distribution: not taxable (return of corpus)
- Unit trust: may be tax-exempt under specific gazette orders (if listed)

**Financial Statements:**
1. Statement of Comprehensive Income
2. Statement of Financial Position
3. Statement of Changes in Net Assets
4. Statement of Cash Flows
5. Notes

**COA considerations:**
- Trust corpus (capital contributed by settlor)
- Accumulated income (undistributed)
- Distributions payable
- Income classified by source (rental, dividend, interest, capital gains)
- Beneficiary accounts (if specific allocation required by deed)

---

## Statutory Deductions — All Entity Types with Employees

| Item | Employer Rate | Employee Rate | Basis |
|---|---|---|---|
| EPF/KWSP | 13% (salary ≤ RM5,000) or 12% (salary > RM5,000) | 11% | Gross remuneration |
| SOCSO/PERKESO (Cat 1) | 1.75% | 0.5% | Max insurable: RM6,000/month |
| EIS/SIP | 0.2% | 0.2% | Max insurable: RM6,000/month |
| PCB/MTD | Per LHDN schedule | Employee bears | Monthly tax deduction |
| HRDF/PSMB | 1% | N/A | Employers with 10+ employees |

**Foreign workers:**
- EPF employer: RM5 (5 sen) per employee (not percentage-based)
- EPF employee: optional (11% if elected)
- SOCSO: Category 2 only (employment injury) — employer 1.25%, employee 0%
- EIS: NOT applicable to foreign workers

**Director (not under contract of service):**
- No SOCSO or EIS obligation
- EPF: voluntary (but commonly contributed)
- PCB: still applicable on director fees/remuneration

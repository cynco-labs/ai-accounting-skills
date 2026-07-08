# Statutory Deductions — Payroll Reference

## EPF / KWSP (Employees Provident Fund)

### Contribution Rates (2024 onwards)

**Employer:**
| Employee Monthly Wages | Employer Rate |
|---|---|
| ≤ RM5,000 | 13% |
| > RM5,000 | 12% |

**Employee:**
| Age | Rate |
|---|---|
| Below 60 | 11% |
| 60 and above | 0% (voluntary up to 11%) |

**Maximum contribution wage:** RM20,000/month (above this, contribute on RM20,000)

**Foreign workers:**
- Employer: RM5 (flat, regardless of salary)
- Employee: voluntary (11% if elected, minimum RM5 if elected)

### EPF Wage Definition
Includes: basic salary, fixed allowances, overtime, commission, bonus, incentives, arrears of wages, director fees, gratuity

Excludes: service charge, tips, retrenchment benefits, retirement benefits (if >10 years service), travel/outstation allowances (actual expenses)

### EPF Contribution Table
EPF uses contribution tables (not exact percentage). The table rounds to specific amounts based on wage bands. For computation purposes, use the percentage — but actual monthly contribution should follow the KWSP table (available at kwsp.gov.my).

### Accounting Treatment
```
Payroll entry (monthly):
  DR 5000 Salary & Wages          [Gross salary]
  DR 5100 EPF - Employer           [Employer portion: 12% or 13%]
    CR 2110 EPF Payable            [Employer + Employee total]
    CR 1000 Bank / 2150 Salary Payable  [Net pay]

When paying EPF:
  DR 2110 EPF Payable
    CR 1000 Bank
```

Due date: 15th of following month. Late payment: dividend rate penalty.

---

## SOCSO / PERKESO (Social Security Organisation)

### Categories

**Category 1:** Employment Injury Scheme + Invalidity Scheme
- Employer: 1.75%
- Employee: 0.5%
- Applicable: employees < 60 years old

**Category 2:** Employment Injury Scheme only
- Employer: 1.25%
- Employee: 0%
- Applicable: employees ≥ 60 (first employed after age 60, or reaching 60 while employed and choosing not to continue invalidity coverage)

### Ceiling
- Maximum insurable earnings: **RM6,000/month** (effective current rates)
- Above RM6,000: contribute on RM6,000 (capped amount)
- Maximum monthly contribution (Cat 1): RM105.00 employer + RM30.00 employee

### Coverage
- Malaysian employees (mandatory)
- Permanent residents (mandatory)
- Foreign workers: Category 2 only (Employment Injury Scheme)
- Self-employed: voluntary (Self-Employment Social Security Act 2017)

### Exclusion
- Directors not under a contract of service
- Domestic servants
- Spouse of employer (if working in same business)

### Contribution Table
SOCSO uses contribution tables based on wage bands (not exact percentage). The table has 39 wage classes. For computation, use the SOCSO rate table (available at perkeso.gov.my).

### Accounting Treatment
```
Payroll entry:
  DR 5110 SOCSO - Employer         [Employer: 1.75%]
  DR 5000 Salary & Wages           [Employee: 0.5% — if deducted from employee]
    CR 2120 SOCSO Payable          [Total: employer + employee]
    
  OR if employer absorbs employee portion:
  DR 5110 SOCSO - Employer         [Full amount: 2.25%]
    CR 2120 SOCSO Payable          [Full amount]
```

Due date: 15th of following month.

---

## EIS / SIP (Employment Insurance System)

### Rates
- Employer: 0.2%
- Employee: 0.2%
- Total: 0.4%

### Ceiling
- Maximum insurable earnings: **RM6,000/month**
- Maximum monthly contribution: RM12.00 employer + RM12.00 employee

### Coverage
- Malaysian employees aged 18-60
- NOT applicable to: foreign workers, domestic servants, self-employed, public sector

### Accounting Treatment
```
  DR 5120 EIS - Employer           [0.2%]
  DR 5000 Salary & Wages           [0.2% employee portion — if deducted]
    CR 2130 EIS Payable            [Total: 0.4%]
    
  OR if employer absorbs:
  DR 5120 EIS - Employer           [Full 0.4%]
    CR 2130 EIS Payable            [Full 0.4%]
```

Due date: 15th of following month.

---

## PCB / MTD (Monthly Tax Deduction)

### How It Works
- Employer deducts estimated income tax monthly from employee's salary
- Based on LHDN's Schedule of Monthly Tax Deductions (Jadual PCB)
- Amount depends on: remuneration, marital status, number of children, EPF/zakat deductions
- Employee provides TP1 form (allowable deductions) and TP3 form (spouse details)

### Calculation Methods
1. **Schedule method:** use LHDN's PCB table (for most employers)
2. **Computerised calculation:** formula-based (for payroll software)

### Key Points
- PCB is a credit against final tax liability (not additional tax)
- If PCB > actual tax: employee gets refund when filing
- If PCB < actual tax: employee pays balance
- Employer must remit by 15th of following month
- Year-end excess: employer must do additional PCB deduction in Dec or do year-end computation (CP38)

### Accounting Treatment
```
  DR 5000 Salary & Wages           [PCB amount — deducted from employee]
    CR 2140 PCB Payable            [Amount to remit to LHDN]
    
When paying LHDN:
  DR 2140 PCB Payable
    CR 1000 Bank
```

### Non-Employment Payments Subject to MTD
- Director fees
- Commission (to non-employees — use CP37)
- Contract payments to non-residents (withholding tax, not PCB — see WHT section)

---

## HRDF / PSMB (Human Resources Development Fund)

### Who Must Register
- Employers in manufacturing sector with 50+ employees, OR
- Employers in manufacturing sector with paid-up capital ≥ RM2.5m and 10-49 employees, OR
- Employers in other sectors (services, mining, etc.) with 10+ employees

### Rate
- 1% of monthly wages of each Malaysian employee
- Employer contribution only (not deducted from employee)

### Accounting Treatment
```
  DR 5130 HRDF Levy                [1% of qualifying wages]
    CR 2160 HRDF Payable           [Amount due]
```

Due date: 15th of following month.

---

## Payroll Processing Checklist

1. **Verify payslip structure:**
   - Gross salary breakdown (basic + allowances)
   - All deductions listed (EPF, SOCSO, EIS, PCB, others)
   - Net pay shown

2. **Cross-reference with bank:**
   - Net pay on payslip = bank payment to employee (± timing difference)
   - Statutory payments from bank = total contributions due

3. **Check for absorption:**
   - If net pay ≈ gross pay (minimal deductions): employer may be absorbing
   - Verify with employee/payroll records

4. **Director vs Employee:**
   - Directors: may only have PCB (no SOCSO/EIS if not under contract)
   - Directors: EPF voluntary (but common)
   - Director fees: lump sum (not monthly salary) → different PCB treatment

5. **Verify ceilings:**
   - EPF: contribution on max RM20,000
   - SOCSO/EIS: contribution on max RM6,000
   - If salary > cap: ensure contributions not over-stated

6. **Year-end:**
   - Total annual EPF employer = 12 or 13% × total qualifying remuneration
   - Total annual SOCSO/EIS within caps
   - Any bonus/13th month: include in month's wages for contribution purposes
   - Verify employer has filed Form E (employer return) by 31 March

---

## Summary Table (Monthly Calculation)

| Component | Formula | Account DR | Account CR |
|---|---|---|---|
| Gross Salary | Per payslip | 5000 | — |
| EPF (Employer) | 12/13% × Gross | 5100 | 2110 |
| EPF (Employee) | 11% × Gross | — | 2110 (from salary) |
| SOCSO (Employer) | 1.75% × min(Gross, 6000) | 5110 | 2120 |
| SOCSO (Employee) | 0.5% × min(Gross, 6000) | — | 2120 (from salary) |
| EIS (Employer) | 0.2% × min(Gross, 6000) | 5120 | 2130 |
| EIS (Employee) | 0.2% × min(Gross, 6000) | — | 2130 (from salary) |
| PCB | Per schedule | — | 2140 (from salary) |
| Net Pay | Gross - Employee EPF - SOCSO - EIS - PCB | — | 1000/2150 |
| HRDF (if applicable) | 1% × Gross | 5130 | 2160 |

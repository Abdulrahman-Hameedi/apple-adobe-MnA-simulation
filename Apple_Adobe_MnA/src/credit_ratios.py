import pandas as pd

def compute_credit_ratios(acquirer, target, deal, proforma):
    # pre-deal vals and post-deal vals

    pre_ebit = acquirer.income["EBIT"].dropna().iloc[-1]
    pre_ebitda = acquirer.income["EBIT"].dropna().iloc[-1] + acquirer.cashflow["Depreciation And Amortization"].dropna().iloc[-1]
    pre_debt = acquirer.balance["Total Debt"].iloc[-1]
    pre_interest = acquirer.income["Interest Expense"].dropna().iloc[-1]
    pre_debt_ebitda = pre_debt/pre_ebitda
    pre_interest_coverage = abs(pre_ebit/pre_interest)

    post_ebit = proforma["EBIT"].iloc[0]
    post_ebitda = post_ebit + acquirer.cashflow["Depreciation And Amortization"].dropna().iloc[-1] + target.cashflow["Depreciation And Amortization"].dropna().iloc[-1]
    post_debt = pre_debt+deal["New Debt"]
    post_interest = post_debt*0.05
    post_debt_ebitda = post_debt/post_ebitda
    post_interest_coverage = post_ebit/post_interest

    return {
        "Pre-Deal Debt/EBITDA": pre_debt_ebitda,
        "Pre-Deal Interest Coverage": pre_interest_coverage,
        "Post-Deal Debt/EBITDA": post_debt_ebitda,
        "Post-Deal Interest Coverage": post_interest_coverage
    }

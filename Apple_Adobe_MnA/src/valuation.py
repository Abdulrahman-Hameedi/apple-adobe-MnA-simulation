import yfinance as yf
import pandas as pd

# risk-free rate: at 4.2% (current)
# equity risk premium: at 5.5% 
# rf and erp will be initialized this way and in the monte carlo simulation they will be randomized
def computeWacc(company, assumptions=None) -> float:
    if assumptions is None:
        from models.assumptions import base_case
        assumptions = base_case
    rf = assumptions["rf"]
    erp = assumptions["erp"]
    beta = company.info["beta"]
    re = rf + beta*(erp)
    interest_exp = company.income["Interest Expense"].dropna().mean()
    total_debt = company.balance["Total Debt"].dropna().mean()
    rd = abs(interest_exp)/total_debt
    tax_prov = company.income["Tax Provision"].dropna().mean()
    pretax_income = company.income["Pretax Income"].dropna().mean()
    tax_rate = tax_prov / pretax_income
    sharesOutstanding = company.info["sharesOutstanding"]
    currPrice = company.info["currentPrice"]
    market_cap = sharesOutstanding*currPrice
    total_debt_recent = company.balance["Total Debt"].dropna().iloc[-1]
    v = market_cap+total_debt_recent
    e_weight = market_cap/v
    d_weight = total_debt_recent/v
    wacc = e_weight*re + d_weight*rd*(1-tax_rate)
    return wacc

def dcf_valuation(company, assumptions=None, wacc_override=None) -> dict:
    if assumptions is None:
        from models.assumptions import base_case
        assumptions = base_case
    terminal_growth = assumptions["terminal_growth"]
    wacc = wacc_override if wacc_override is not None else computeWacc(company, assumptions)
    projFCF = company.forecast["FCF"]
    
    # discount each fcf back to present val
    pv = [] # present values
    for i, fcf in enumerate(projFCF, start=1):
        pv.append(fcf/(1+wacc)**i)
    last_fcf = projFCF.iloc[-1]
    terminal_val = last_fcf*(1+terminal_growth)/(wacc-terminal_growth)
    TV_discounted = terminal_val/(1+wacc)**5
    enterprise_val = sum(pv)+TV_discounted
    total_debt = company.balance["Total Debt"].dropna().iloc[-1]
    cash = company.balance["Cash And Cash Equivalents"].dropna().iloc[-1]
    net_debt = total_debt - cash
    equity_val = enterprise_val - net_debt
    intrinsic_val_per_share = equity_val/company.info["sharesOutstanding"]

    return {
        "WACC": wacc,
        "Enterprise Value": enterprise_val,
        "Net Debt": net_debt,
        "Equity Value": equity_val,
        "Intrinsic Value Per Share": intrinsic_val_per_share
    }
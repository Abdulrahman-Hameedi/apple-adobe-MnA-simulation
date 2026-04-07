import numpy_financial as npf
from src.valuation import computeWacc

def compute_irr(target, deal, synergies, assumptions):
    purchase_price = -deal["Purchase Price"]
    terminal_val = ((target.forecast["FCF"].iloc[-1])*(1+assumptions["terminal_growth"]))/(computeWacc(target, assumptions)-assumptions["terminal_growth"])
    cashflows = [purchase_price]
    for year in range(1, 6):
        if year in [1, 2]:
            cashflows.append(
                target.forecast["FCF"].iloc[year-1] +
                synergies["Cost Synergies"].iloc[year-1] +
                synergies["Revenue Synergies"].iloc[year-1] -
                synergies["Integration Costs"].iloc[year-1]
            )
        if year in [3,4]:
            cashflows.append(target.forecast["FCF"].iloc[year-1] + synergies["Cost Synergies"].iloc[year-1] + synergies["Revenue Synergies"].iloc[year-1])
        if year == 5:
            fcf = target.forecast["FCF"].iloc[-1]
            syn = synergies["Cost Synergies"].iloc[-1] + synergies["Revenue Synergies"].iloc[-1]
            cashflows.append(fcf + syn + terminal_val)
    return npf.irr(cashflows)

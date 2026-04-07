import pandas as pd

def build_proforma(acquirer, target, deal, synergies, interest_rate=0.05) -> pd.DataFrame:
    acquirer_forecast_rev, acquirer_forecast_EBIT = acquirer.forecast["Revenue"], acquirer.forecast["EBIT"]
    target_forecast_rev, target_forecast_EBIT = target.forecast["Revenue"], target.forecast["EBIT"]
    rev_synergies = synergies["Revenue Synergies"]
    cost_synergies = synergies["Cost Synergies"]
    integ_costs_synergies = synergies["Integration Costs"]
    combinedRev = acquirer_forecast_rev + target_forecast_rev + rev_synergies
    combinedEbit = acquirer_forecast_EBIT + target_forecast_EBIT + cost_synergies - integ_costs_synergies
    interest_expense = deal["New Debt"]*interest_rate
    # blended tax rate
    acquirer_tax = (acquirer.income["Tax Provision"] / acquirer.income["Pretax Income"]).dropna().mean()
    target_tax = (target.income["Tax Provision"] / target.income["Pretax Income"]).dropna().mean()
    blended_tax = (acquirer_tax+target_tax)/2
    # combined net income
    combined_net_income = (combinedEbit-interest_expense)*(1-blended_tax)
    # pro forma shares and EPS
    proforma_shares = acquirer.info["sharesOutstanding"] + deal["New Shares Issued"]
    proforma_eps = combined_net_income/proforma_shares
    return pd.DataFrame({
        "Revenue": combinedRev,
        "EBIT": combinedEbit,
        "Net Income": combined_net_income,
        "EPS": proforma_eps
    })

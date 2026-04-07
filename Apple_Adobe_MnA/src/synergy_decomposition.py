import pandas as pd
from src.valuation import dcf_valuation

def synergy_npv_decomposition(acquirer, target, deal, synergies, assumptions, years):
    acquirer_dcf = dcf_valuation(acquirer, assumptions)
    acquirer_equity_val = acquirer_dcf["Equity Value"]
    target_equity_val = dcf_valuation(target, assumptions)["Equity Value"]
    purchase_price = deal["Purchase Price"]
    premium = purchase_price - target_equity_val
    wacc = acquirer_dcf["WACC"]

    # discount each yr's synergies back to present value
    npv_cost = sum([synergies["Cost Synergies"].iloc[i]/(1+wacc)**(i+1) for i in range(years)])
    npv_revenue = sum([synergies["Revenue Synergies"].iloc[i] / (1 + wacc) ** (i + 1) for i in range(years)])
    npv_integration = sum([synergies["Integration Costs"].iloc[i] / (1 + wacc) ** (i + 1) for i in range(years)])

    tot_syn_val = npv_cost+npv_revenue-npv_integration
    net_val_created = tot_syn_val-premium

    result = {
        "Standalone Apple Equity Value": acquirer_equity_val,
        "Standalone Adobe Equity Value": target_equity_val,
        "Purchase Price": purchase_price,
        "Premium Paid": premium,
        "NPV Cost Synergies": npv_cost,
        "NPV Revenue Synergies": npv_revenue,
        "NPV Integration Costs": npv_integration,
        "Total Synergy Value": tot_syn_val,
        "Net Value Created": net_val_created
    }
    print(f"\n——Synergy NPV Decompostion - {years} Year Model——")
    for k,v in result.items():
        if k == "Premium Paid":
            label = "Premium Paid" if premium > 0 else "Discount to Intrinsic Value"
            print(f"{label:<35} ${abs(v)/1e9:.2f}B")
        else:
            print(f"{k:<35} ${v/1e9:.2f}B")
    return result
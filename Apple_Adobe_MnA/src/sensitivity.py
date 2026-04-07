import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.valuation import dcf_valuation
from src.deal import structure_deal
from src.synergies import compute_synergies
from src.proforma import build_proforma
from src.accretion import accretion_dilution
from src.forecasting import forecast_company 

# this file will test the sensitivity of acqiurer company's intrinsic value to changes in WACC and terminal growth rate

def wacc_vs_terminal_growth(company, assumptions):
    wacc_range = np.arange(0.07, 0.14, 0.01)
    # 3 percentage points: 7% (optimistic) to 13% (pessimistic)
    # the WACC at first came out as 10%; hence these assumptions
    term_growth_range = np.arange(0.01, 0.05, 0.005)
    results = pd.DataFrame(index=[f"{w:.0%}" for w in wacc_range],
                           columns=[f"{g:.1%}" for g in term_growth_range])
    for w in wacc_range:
        for g in term_growth_range:
            modified = {**assumptions, "terminal_growth": g}
            val = dcf_valuation(company, modified, wacc_override=w)
            results.loc[f"{w:.0%}",f"{g:.1%}"] = round(val["Intrinsic Value Per Share"], 2)
    results = results.astype(float)
    plt.figure(figsize=(12,6))
    sns.heatmap(results, annot=True, fmt=".0f", cmap="RdYlGn")
    plt.title("Apple Intrinsic Value Per Share - WACC vs Terminal Growth")
    plt.xlabel("Terminal Growth Rate")
    plt.ylabel("WACC")
    plt.tight_layout()
    plt.show()
    return results

def premium_vs_synergy(acquirer, target, assumptions):
    premium_range = np.arange(0.10, 0.45, 0.05)
    syn_range = np.arange(0.50, 1.51, 0.25)

    results = pd.DataFrame(index=[f"{p:.0%}" for p in premium_range],
                           columns=[f"{s:.0%}" for s in syn_range])
    for p in premium_range:
        for s in syn_range:
            modified = {**assumptions, "premium":p}
            target.forecast = forecast_company(target, 5)
            deal = structure_deal(acquirer, target, modified)
            syn = compute_synergies(target, assumptions=modified) * s
            proforma = build_proforma(acquirer, target, deal, syn)
            acc_dil = accretion_dilution(acquirer, proforma)
            results.loc[f"{p:.0%}", f"{s:.0%}"] = round(acc_dil["Accretion/Dilution %"].iloc[-1], 2)
    results = results.astype(float)
    plt.figure(figsize=(12,6))
    sns.heatmap(results, annot=True, fmt=".1f", cmap="RdYlGn", center=0)
    plt.title("Year 5 Accretion % - Acquisition Premium vs Synergy Realization")
    plt.xlabel("Synergy Realization")
    plt.ylabel("Acquisition Premium")
    plt.tight_layout()
    plt.show()
    return results
    
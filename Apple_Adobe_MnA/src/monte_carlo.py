import pandas as pd
import numpy as np
from src.forecasting import forecast_company
from src.synergies import compute_synergies
from src.proforma import build_proforma
from src.accretion import accretion_dilution
from src.valuation import computeWacc

def monte_carlo(acquirer, target, deal, assumptions=None) -> pd.DataFrame:
    results = []
    base_wacc = computeWacc(acquirer)
    if assumptions is None:
        from models.assumptions import base_case
        assumptions = base_case
    n_simulations = assumptions["n_simulations"]
    for _ in range(n_simulations):
        wacc_shock = np.random.normal(0, 0.01)
        cagr_shock = np.random.normal(0, 0.01)
        syn_realization = np.random.normal(1.0, 0.10)

        # forecast with shocked cagr
        acquirer.forecast = forecast_company(acquirer, 5, cagr_shock)
        target.forecast = forecast_company(target, 5, cagr_shock)

        # recompute synergies scaled by syn realization
        syn = compute_synergies(target, 5, assumptions=None) * syn_realization

        # rebuild pro forma with shocked wacc
        interest_rate = 0.05+wacc_shock
        proforma = build_proforma(acquirer, target, deal, syn, interest_rate)

        # compute accretion/dilution
        acc_dil = accretion_dilution(acquirer, proforma)

        results.append(acc_dil["Accretion/Dilution %"].iloc[-1])
    return pd.DataFrame(results, columns=["Year 5 Accretion %"])

def probability_metrics(mc_results, wacc) -> dict:
    prob_acc_less_zero = (mc_results["Year 5 Accretion %"]<0).mean()
    prob_acc_less_two = (mc_results["Year 5 Accretion %"]<2).mean()
    prob_acc_great_five = (mc_results["Year 5 Accretion %"]>5).mean()
    results = {
        "P(accretion < 0)": prob_acc_less_zero,
        "P(accretion < 2)": prob_acc_less_two,
        "P(accretion > 5)": prob_acc_great_five
    }
    return results

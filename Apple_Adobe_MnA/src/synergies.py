import pandas as pd

def compute_synergies(target, years=5,
                      assumptions=None
                      ) -> pd.DataFrame:
    if assumptions is None:
        from models.assumptions import base_case
        assumptions = base_case
    cost_syn_perc = assumptions["cost_syn_perc"]
    rev_syn_perc = assumptions["rev_syn_perc"]
    integration_cost_perc = assumptions["integration_cost_perc"]
    
    target_avg_SGnA = target.income["Selling General And Administration"].dropna().mean()
    full_cost_synergy = target_avg_SGnA*cost_syn_perc
    increment = [0.25, 0.75] + [1.0]*(years-2)
    cost_synergies = [full_cost_synergy*increment[i] for i in range(len(increment))]
    projRev = target.forecast["Revenue"]
    full_rev_synergy_perYr = projRev*rev_syn_perc
    rev_syn_perYr = [full_rev_synergy_perYr.iloc[i] * increment[i] for i in range(years)]
    integration_costs = []
    for i in range(1, years + 1):
        if i == 1 or i == 2:
            integration_costs.append(projRev.iloc[i-1]*integration_cost_perc)
        else:
            integration_costs.append(0)
    lastYr = target.income["Total Revenue"].dropna().index[-1]
    idx = [lastYr+i for i in range(1, years+1)]
    data = {
        "Cost Synergies": cost_synergies,
        "Revenue Synergies": rev_syn_perYr,
        "Integration Costs": integration_costs
    }
    return pd.DataFrame(data, index=idx)

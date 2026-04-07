base_case = {
    # forecast
    "revenue_cagr_adjustment": 0.0,
    "terminal_growth": 0.03, # 3% growth
    "rf": 0.042, # current US 10-year treasury
    "erp": 0.055, # historical US equity risk premium
    # deal
    "premium": 0.25, # 25% acquisition premium
    "cash_perc": 0.50,
    "interest_rate": 0.05, # cost of new debt
    # synergies
    "cost_syn_perc": 0.20, # 20% of adobe sg&a
    "rev_syn_perc": 0.03, # 3% additional revenue growth
    "integration_cost_perc": 0.05, # 5% of revenue
    # Monte carlo
    "n_simulations": 500,
    "wacc_std": 0.01,
    "cagr_std": 0.01,
    "syn_std": 0.10
}
bull_case = {
    **base_case,
    "revenue_cagr_adjustment": 0.02, # 2% faster growth than historical
    "premium": 0.20, # lower premium = better deal
    "cost_syn_perc": 0.30, 
    "rev_syn_perc": 0.05,
    "integration_cost_perc": 0.03 # cheaper integration
}
bear_case = {
    **base_case,
    "revenue_cagr_adjustment": -0.02,
    "premium": 0.30,
    "cost_syn_perc": 0.10,
    "rev_syn_perc": 0.01,
    "integration_cost_perc": 0.08
}
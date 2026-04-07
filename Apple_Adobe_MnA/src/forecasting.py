import pandas as pd

def forecast_company(company, years = 5, cagr_shock=0.0) -> pd.DataFrame:
    total_revenue = company.income["Total Revenue"].dropna()
    EBIT = company.income["EBIT"].dropna()
    lastVal, firstVal = total_revenue.iloc[-1], total_revenue.iloc[0]
    nYrs = len(total_revenue) - 1
    cagr = (lastVal/firstVal)**(1/nYrs) - 1
    lastYr = total_revenue.index[-1]
    futureYrs = [lastYr + i for i in range(1, years+1)]
    CAGR_adjusted = cagr + cagr_shock
    projRevenue = [lastVal * (1+CAGR_adjusted)**i for i in range(1, years+1)]
    common_idx_ebit = total_revenue.index.intersection(EBIT.index)
    avg_ebit_margin = (EBIT.loc[common_idx_ebit] / total_revenue.loc[common_idx_ebit]).mean()
    projEBIT = [r*avg_ebit_margin for r in projRevenue]
    net_income = company.income["Net Income"].dropna()
    common_idx = total_revenue.index.intersection(net_income.index)
    avg_net_margin = (net_income.loc[common_idx] / total_revenue.loc[common_idx]).mean()
    projNetIncome = [r*avg_net_margin for r in projRevenue]

    # FCF = operating cashflow - CapEx
    op_cashflow = company.cashflow["Operating Cash Flow"].dropna()
    capex = company.cashflow["Capital Expenditure"].dropna()
    common_idx_fcf = total_revenue.index.intersection(op_cashflow.index).intersection(capex.index)
    avg_fcf_margin = ((op_cashflow.loc[common_idx_fcf] - capex.abs().loc[common_idx_fcf]) / total_revenue.loc[common_idx_fcf]).mean()
    projFCF = [r*avg_fcf_margin for r in projRevenue]

    idx = futureYrs
    data = {
        "Revenue": projRevenue,
        "EBIT": projEBIT,
        "Net Income": projNetIncome,
        "FCF": projFCF
        }
    return pd.DataFrame(data, index=idx)
    

import yfinance as yf
import pandas as pd
import os

def load_financials(ticker: str) -> dict:
    company = yf.Ticker(ticker)
    raw = {
        "income": company.financials.T,
        "balance": company.balance_sheet.T,
        "cashflow": company.cashflow.T
    }
    cleaned = {}
    for k, df in raw.items():
        df.index = df.index.year # YYYY/MM/DD -> YYYY
        df = df.sort_index()
        df = df.dropna(axis=1, how="all")
        cleaned[k] = df
    return cleaned

def save_financials(ticker: str, data: dict, path: str = "data/raw") -> None:
    os.makedirs(path, exist_ok=True)
    tick = ticker.lower()
    for k, df in data.items():
        fn = f"{tick}_{k}.csv"
        fp = os.path.join(path, fn)
        df.to_csv(fp)
        print(f"Saved {fp}")

if __name__ == '__main__':
    pass
    # data = load_financials("AAPL")
    # print(data["income"].shape)
    # print(data["income"].columns.tolist())
    # print(data["income"].index)
    # print(data["income"].head())
    # print(data["income"].index.tolist())
    # print(data["income"][["Total Revenue", "Gross Profit", "Operating Income", "Net Income"]].round(2))
    # for ticker in ["AAPL", "ADBE"]:
       # data = load_financials(ticker)
       # save_financials(ticker, data)
    '''
    Shape (5, 39) - 5 years of data, 39 line items
    dates are like 2025-09-30 - Apple's fiscal year ends in September
    '''

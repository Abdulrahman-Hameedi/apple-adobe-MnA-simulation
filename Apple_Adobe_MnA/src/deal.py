import pandas as pd

# assume premium = 25%
# cash fraction = 50%
def structure_deal(acquirer, target, assumptions=None) -> dict:
    if assumptions is None:
        from models.assumptions import base_case
        assumptions = base_case
    premium = assumptions["premium"]
    cash_perc = assumptions["cash_perc"]
    target_market_cap = target.info["sharesOutstanding"]*target.info["currentPrice"]
    purchase_price = target_market_cap*(1+premium)
    cash_portion = purchase_price*cash_perc
    stock_portion = purchase_price*(1-cash_perc)
    new_shares_issued = stock_portion/acquirer.info["currentPrice"]
    target_price_paid = target.info["currentPrice"] + (1+premium)
    exchange_ratio = target_price_paid/acquirer.info["currentPrice"]
    new_debt = cash_portion
    book_equity = target.balance["Total Assets"].dropna().iloc[-1] - target.balance["Total Liabilities Net Minority Interest"].dropna().iloc[-1]
    goodwill = purchase_price - book_equity
    return {
        "Target Market Cap": target_market_cap,
        "Purchase Price": purchase_price,
        "Cash Portion": cash_portion,
        "Stock Portion": stock_portion,
        "New Shares Issued": new_shares_issued,
        "Exchange Ratio": exchange_ratio,
        "New Debt": new_debt,
        "Book Equity": book_equity,
        "Goodwill": goodwill
    }
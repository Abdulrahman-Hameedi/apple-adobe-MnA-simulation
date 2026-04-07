import pandas as pd
import yfinance as yf

class Company:
    def __init__(self, name: str, ticker: str, financials: dict):
        self.name = name
        self.financials = financials
        self.income = financials["income"]
        self.balance = financials["balance"]
        self.cashflow = financials["cashflow"]
        self.info = yf.Ticker(ticker).info
        self.forecast = None


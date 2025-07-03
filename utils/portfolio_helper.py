# utils/portfolio_helper.py

import yfinance as yf
import random

def get_mock_financial_metrics(ticker):
    """
    Returns mocked financial metrics for Indian market tickers.
    Useful for demo or when real data is unavailable.
    """
    return {
        "Revenue": round(random.uniform(50000, 200000), 2),      # in ₹ Crores approx
        "Net Profit": round(random.uniform(5000, 50000), 2),
        "EPS": round(random.uniform(10, 100), 2)
    }

def get_financial_metrics_yfinance(ticker):
    """
    Fetch financial metrics for foreign market tickers from Yahoo Finance.
    Returns Revenue, Net Profit, and EPS (trailing).
    """
    try:
        stock = yf.Ticker(ticker)
        
        revenue = None
        net_income = None
        
        try:
            financials = stock.financials
            if not financials.empty:
                revenue = financials.loc["Total Revenue"].values[0] if "Total Revenue" in financials.index else None
                net_income = financials.loc["Net Income"].values[0] if "Net Income" in financials.index else None
        except Exception:
            pass  # fail silently if financials not available
        
        info = stock.info
        eps = info.get("trailingEps")

        return {
            "Revenue": round(revenue / 1e7, 2) if revenue else None,     # Convert to ₹ Crores
            "Net Profit": round(net_income / 1e7, 2) if net_income else None,
            "EPS": round(eps, 2) if eps else None
        }
    except Exception as e:
        print(f"[Error] Fetching financials for {ticker}: {e}")
        return {"Revenue": None, "Net Profit": None, "EPS": None}

def get_historical_data(ticker):
    """
    Generates mock historical financial data for plotting trend charts.
    Returns a dict with Year, Revenue, Net Profit, EPS lists.
    """
    years = ["2020", "2021", "2022", "2023", "2024"]
    return {
        "Year": years,
        "Revenue": [round(random.uniform(10000, 100000), 2) for _ in years],
        "Net Profit": [round(random.uniform(1000, 20000), 2) for _ in years],
        "EPS": [round(random.uniform(10, 50), 2) for _ in years]
    }

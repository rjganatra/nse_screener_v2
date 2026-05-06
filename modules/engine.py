import yfinance as yf
import pandas as pd
import requests_cache
from datetime import timedelta

# CRITICAL: This caches API calls for 7 days so you don't get banned.
# Price data will be fetched fresh, but fundamentals will be cached.
session = requests_cache.CachedSession('screener_cache', expire_after=timedelta(days=7))
session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

def analyze_stock(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol, session=session)
        info = stock.info
        
        # 1. Price vs 52-Week Low (Technical)
        current_price = info.get('previousClose', 0)
        low_52wk = info.get('fiftyTwoWeekLow', 0)
        
        if low_52wk == 0 or current_price == 0:
            return None
            
        # Is price within 30% of 52-week low?
        margin_from_low = (current_price - low_52wk) / low_52wk
        if margin_from_low > 0.30:
            return None # Fails technical criteria

        # 2. Fundamentals (ROE > ROCE, Low Debt)
        roe = info.get('returnOnEquity', 0)
        roce = info.get('returnOnAssets', 0) # yfinance proxy for ROCE
        debt_to_equity = info.get('debtToEquity', 100) # Default to 100 (bad) if missing
        
        # Apply your rules
        if (roe is not None and roce is not None and roe > roce) and (debt_to_equity < 30):
            return {
                'Ticker': ticker_symbol,
                'Price': current_price,
                '52W_Low': low_52wk,
                'ROE': round(roe * 100, 2) if roe else 0,
                'Debt/Equity': debt_to_equity
            }
        return None
        
    except Exception as e:
        # Silently fail on bad tickers to keep the loop running
        return None

import pandas as pd
import requests

def get_nifty_500_tickers():
    print("Fetching latest Nifty 500 universe from NSE...")
    url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        with open("nifty500.csv", "wb") as f:
            f.write(response.content)
            
        df = pd.read_csv("nifty500.csv")
        # Add .NS for Yahoo Finance compatibility
        tickers = df['Symbol'].apply(lambda x: f"{x}.NS").tolist()
        return tickers
    except Exception as e:
        print(f"Error fetching universe: {e}")
        return []

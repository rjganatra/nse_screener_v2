import pandas as pd
from modules.universe import get_nifty_500_tickers
from modules.engine import analyze_stock
from modules.alerts import send_telegram_alert
import time

def main():
    print("Starting NSE Analyzer Pipeline...")
    
    # 1. Get Universe
    tickers = get_nifty_500_tickers()
    
    # For testing, just run the first 20 so it doesn't take hours. 
    # Remove the [:20] when you are ready to scan all 500.
    test_universe = tickers[:20] 
    
    passed_stocks = []
    
    # 2. Analyze
    print(f"Scanning {len(test_universe)} stocks...")
    for ticker in test_universe:
        result = analyze_stock(ticker)
        if result:
            passed_stocks.append(result)
        # Small delay to mimic human browsing
        time.sleep(0.5) 
            
    # 3. Format and Alert
    df = pd.DataFrame(passed_stocks)
    print("\n--- Scan Complete ---")
    print(df)
    
    send_telegram_alert(df)

if __name__ == "__main__":
    main()

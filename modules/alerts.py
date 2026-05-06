import requests
import os

def send_telegram_alert(passing_stocks_df):
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        print("Telegram credentials not found in environment.")
        return
        
    if passing_stocks_df.empty:
        message = "📉 NSE Screener Run Complete: No stocks met the strict criteria today."
    else:
        message = "🚀 **NSE Screener Results**\n\n"
        for index, row in passing_stocks_df.iterrows():
            message += f"**{row['Ticker']}**\n"
            message += f"Price: ₹{row['Price']} (52W Low: ₹{row['52W_Low']})\n"
            message += f"ROE: {row['ROE']}% | D/E: {row['Debt/Equity']}\n\n"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

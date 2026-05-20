import os
import requests
import pandas as pd
import time

def download_data():
    coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT", "DOTUSDT", "DOGEUSDT", "AVAXUSDT", "MATICUSDT", "LINKUSDT"]
    interval = "1d"
    limit = 1000  # maximum allowed by Binance for one request, good for backtesting

    if not os.path.exists("data"):
        os.makedirs("data")

    for symbol in coins:
        print(f"Downloading {symbol}...")
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        url = "https://api.binance.com/api/v3/klines"
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data, columns=[
                    "Open time", "Open", "High", "Low", "Close", "Volume", 
                    "Close time", "Quote asset volume", "Number of trades", 
                    "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
                ])
                df["Date"] = pd.to_datetime(df["Open time"], unit="ms")
                for col in ["Open", "High", "Low", "Close", "Volume"]:
                    df[col] = df[col].astype(float)
                
                df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
                df.to_csv(f"data/{symbol}.csv", index=False)
                print(f"Saved {symbol}.csv")
            else:
                print(f"Error {response.status_code} for {symbol}")
        except Exception as e:
            print(f"Failed to download {symbol}: {e}")
        time.sleep(1) # wait 1s between requests to avoid rate limits

if __name__ == '__main__':
    download_data()

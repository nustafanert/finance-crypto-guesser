import requests


def get_binance_klines(symbol="BTCUSDT", interval="1h", limit=50):
    # Binance uzerinden gecmis kapanis verilerini (kline/candlestick) ceker
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"

    try:
        response = requests.get(url)
        data = response.json()

        # Sadece kapanis fiyatlarini (index 4) alip listeye ekliyoruz
        closing_prices = []
        for candle in data:
            closing_prices.append(float(candle[4]))

        print(
            f"Successfully fetched {len(closing_prices)} historical prices from Binance for {symbol}."
        )
        return closing_prices
    except Exception as e:
        print("Error fetching data from Binance:", e)
        return []


if __name__ == "__main__":
    prices = get_binance_klines()
    print("Last 5 closing prices:", prices[-5:])

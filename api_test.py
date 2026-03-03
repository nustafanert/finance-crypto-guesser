import requests


# Bu fonksiyon Binance'den anlik Bitcoin fiyatini ceker
def get_crypto_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

    try:
        response = requests.get(url)
        data = response.json()
        price = float(data["price"])
        print(f"Current {symbol} Price is: {price}")
        return price
    except Exception as e:
        print("Error fetching data:", e)
        return None


# Test edelim
if __name__ == "__main__":
    get_crypto_price("BTCUSDT")

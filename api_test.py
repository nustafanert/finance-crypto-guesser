import requests


def test_coingecko_api():
    # CoinGecko'dan anlik fiyatlari ceken basit uc (endpoint)
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        print("CoinGecko API Response Success!")
        print(f"Bitcoin Price: ${data['bitcoin']['usd']}")
        print(f"Ethereum Price: ${data['ethereum']['usd']}")
    except Exception as e:
        print("Error connecting to CoinGecko:", e)


if __name__ == "__main__":
    test_coingecko_api()

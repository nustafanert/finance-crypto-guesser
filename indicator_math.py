# Basit Hareketli Ortalama (SMA) Indikatoru
def calculate_sma(prices, period):
    # Eger elimizde yeterli fiyat verisi yoksa hesaplama yapma
    if len(prices) < period:
        print("Not enough data to calculate SMA")
        return None

    # Sadece son 'period' kadar fiyati al
    recent_prices = prices[-period:]
    total = sum(recent_prices)
    sma = total / period

    print(f"SMA for period {period} is: {sma}")
    return sma


# Sahte verilerle test edelim (Gercekte bu veriler Binance'den gelecek)
if __name__ == "__main__":
    sample_prices = [90000, 91000, 90500, 92000, 93000]
    calculate_sma(sample_prices, 3)  # Son 3 periyodun ortalamasi

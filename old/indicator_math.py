def calculate_sma(prices, period=14):
    # Elimizde yeterli veri yoksa uyari ver
    if len(prices) < period:
        print("Not enough data to calculate SMA")
        return None
    
    # Sadece son 'period' kadar fiyati al ve ortalamasini hesapla
    recent_prices = prices[-period:]
    sma = sum(recent_prices) / period
    
    print(f"Calculated SMA for last {period} periods is: {sma:.2f}")
    return sma

if __name__ == "__main__":
    # Kodun calisip calismadigini test etmek icin ornek veriler
    sample_prices = [90000, 91000, 90500, 92000, 93000, 92500, 94000]
    calculate_sma(sample_prices, 3)
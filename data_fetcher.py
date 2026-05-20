import pandas as pd
import os
from datetime import datetime

def get_binance_data(symbol="BTCUSDT", interval="1d", limit=365):
    """
    Yerel CSV dosyasından kline (mum) verilerini çeker (Offline Mod).
    Varsayılan: Son 1 yılın (365 gün) günlük verisi.
    """
    file_path = f"data/{symbol}.csv"
    
    if not os.path.exists(file_path):
        raise Exception(f"Offline veri bulunamadı: {file_path}. Lütfen önce verileri indirin.")
        
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    
    # İstenen limit kadar son veriyi döndür
    if len(df) > limit:
        df = df.tail(limit).reset_index(drop=True)
        
    return df
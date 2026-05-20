import pandas as pd
import ta

def calculate_indicators(df):
    """Adds technical indicators to the given DataFrame."""
    df = df.copy()
    
    df['SMA_10'] = ta.trend.sma_indicator(df['Close'], window=10)
    df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
    
    df['EMA_9'] = ta.trend.ema_indicator(df['Close'], window=9)
    df['EMA_21'] = ta.trend.ema_indicator(df['Close'], window=21)
    
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    
    df['MACD'] = ta.trend.macd(df['Close'])
    df['MACD_Signal'] = ta.trend.macd_signal(df['Close'])
    
    bb = ta.volatility.BollingerBands(df['Close'])
    df['BB_High'] = bb.bollinger_hband()
    df['BB_Low'] = bb.bollinger_lband()
    
    stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'])
    df['Stoch_K'] = stoch.stoch()
    
    adx = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'])
    df['ADX'] = adx.adx()
    
    df['CCI'] = ta.trend.cci(df['High'], df['Low'], df['Close'])

    df['Williams_R'] = ta.momentum.williams_r(df['High'], df['Low'], df['Close'])

    df['AO'] = ta.momentum.awesome_oscillator(df['High'], df['Low'])

    ichimoku = ta.trend.IchimokuIndicator(df['High'], df['Low'])
    df['Ichimoku_Conv'] = ichimoku.ichimoku_conversion_line()
    df['Ichimoku_Base'] = ichimoku.ichimoku_base_line()

    df['MFI'] = ta.volume.money_flow_index(df['High'], df['Low'], df['Close'], df['Volume'])

    df['PSAR'] = ta.trend.psar_up(df['High'], df['Low'], df['Close']).fillna(
        ta.trend.psar_down(df['High'], df['Low'], df['Close'])
    )
    
    return df

def get_consensus_for_row(row, active_indicators, mode="Balanced"):
    votes = {"BUY": 0, "SELL": 0, "NEUTRAL": 0}
    details = {}

    if "SMA Cross" in active_indicators:
        if row['SMA_10'] > row['SMA_50']:
            votes["BUY"] += 1
            details["SMA"] = "BUY (SMA 10 > SMA 50)"
        else:
            votes["SELL"] += 1
            details["SMA"] = "SELL (SMA 10 < SMA 50)"

    if "EMA Cross" in active_indicators:
        if row['EMA_9'] > row['EMA_21']:
            votes["BUY"] += 1
            details["EMA"] = "BUY (EMA 9 > EMA 21)"
        else:
            votes["SELL"] += 1
            details["EMA"] = "SELL (EMA 9 < EMA 21)"

    if "RSI" in active_indicators:
        if row['RSI'] < 30:
            votes["BUY"] += 1
            details["RSI"] = f"BUY (Oversold: {row['RSI']:.1f})"
        elif row['RSI'] > 70:
            votes["SELL"] += 1
            details["RSI"] = f"SELL (Overbought: {row['RSI']:.1f})"
        else:
            votes["NEUTRAL"] += 1
            details["RSI"] = f"NEUTRAL (Normal: {row['RSI']:.1f})"

    if "MACD" in active_indicators:
        if row['MACD'] > row['MACD_Signal']:
            votes["BUY"] += 1
            details["MACD"] = "BUY (Positive Momentum)"
        else:
            votes["SELL"] += 1
            details["MACD"] = "SELL (Negative Momentum)"

    if "Bollinger Bands" in active_indicators:
        if row['Close'] < row['BB_Low']:
            votes["BUY"] += 1
            details["BB"] = "BUY (Price below Lower Band)"
        elif row['Close'] > row['BB_High']:
            votes["SELL"] += 1
            details["BB"] = "SELL (Price above Upper Band)"
        else:
            votes["NEUTRAL"] += 1
            details["BB"] = "NEUTRAL (Inside Bands)"

    if "Stochastic" in active_indicators:
        if row['Stoch_K'] < 20:
            votes["BUY"] += 1
            details["Stoch"] = f"BUY (Oversold: {row['Stoch_K']:.1f})"
        elif row['Stoch_K'] > 80:
            votes["SELL"] += 1
            details["Stoch"] = f"SELL (Overbought: {row['Stoch_K']:.1f})"
        else:
            votes["NEUTRAL"] += 1
            details["Stoch"] = f"NEUTRAL (Normal: {row['Stoch_K']:.1f})"

    if "ADX (Trend)" in active_indicators:
        if row['ADX'] > 25:
            details["ADX"] = f"STRONG TREND ({row['ADX']:.1f})"
            votes["BUY"] += 0.5
        else:
            details["ADX"] = f"WEAK TREND ({row['ADX']:.1f})"
            votes["NEUTRAL"] += 1

    if "CCI" in active_indicators:
        if row['CCI'] < -100:
            votes["BUY"] += 1
            details["CCI"] = f"BUY (Low CCI: {row['CCI']:.1f})"
        elif row['CCI'] > 100:
            votes["SELL"] += 1
            details["CCI"] = f"SELL (High CCI: {row['CCI']:.1f})"
        else:
            votes["NEUTRAL"] += 1
            details["CCI"] = f"NEUTRAL (Normal CCI)"

    if "Williams %R" in active_indicators:
        if row['Williams_R'] < -80:
            votes["BUY"] += 1
            details["WillR"] = f"BUY (Oversold: {row['Williams_R']:.1f})"
        elif row['Williams_R'] > -20:
            votes["SELL"] += 1
            details["WillR"] = f"SELL (Overbought: {row['Williams_R']:.1f})"
        else:
            votes["NEUTRAL"] += 1
            details["WillR"] = f"NEUTRAL (Normal)"

    if "Awesome Oscillator" in active_indicators:
        if row['AO'] > 0:
            votes["BUY"] += 1
            details["AO"] = "BUY (Positive Momentum)"
        else:
            votes["SELL"] += 1
            details["AO"] = "SELL (Negative Momentum)"

    if "Ichimoku" in active_indicators:
        if row['Ichimoku_Conv'] > row['Ichimoku_Base']:
            votes["BUY"] += 1
            details["Ichimoku"] = "BUY (Tenkan > Kijun)"
        else:
            votes["SELL"] += 1
            details["Ichimoku"] = "SELL (Tenkan < Kijun)"

    if "MFI (Money Flow)" in active_indicators:
        if row['MFI'] < 20:
            votes["BUY"] += 1
            details["MFI"] = f"BUY (Capital Inflow: {row['MFI']:.1f})"
        elif row['MFI'] > 80:
            votes["SELL"] += 1
            details["MFI"] = f"SELL (Capital Outflow: {row['MFI']:.1f})"
        else:
            votes["NEUTRAL"] += 1
            details["MFI"] = "NEUTRAL"

    if "Parabolic SAR" in active_indicators:
        if row['Close'] > row['PSAR']:
            votes["BUY"] += 1
            details["PSAR"] = "BUY (Price above SAR)"
        else:
            votes["SELL"] += 1
            details["PSAR"] = "SELL (Price below SAR)"

    total_active = len(active_indicators)
    if total_active == 0: return 0, 0, {}

    if mode == "Aggressive":
        total_vocal = votes["BUY"] + votes["SELL"]
        if total_vocal == 0:
            buy_percent = 50
        else:
            buy_percent = (votes["BUY"] / total_vocal) * 100
    elif mode == "Balanced":
        buy_percent = ((votes["BUY"] + (votes["NEUTRAL"] * 0.5)) / total_active) * 100
    else: # Conservative
        buy_percent = (votes["BUY"] / total_active) * 100

    sell_percent = 100 - buy_percent

    return buy_percent, sell_percent, details

def get_live_consensus(df, active_indicators, mode="Balanced"):
    """
    Analyzes the latest day data based on selected indicators.
    Returns % BUY and % SELL rates.
    """
    last_row = df.iloc[-1]
    return get_consensus_for_row(last_row, active_indicators, mode)

def run_backtest(df, active_indicators, mode="Balanced", initial_balance=1000):
    balance = initial_balance
    crypto_held = 0
    trade_log = []
    
    current_buy = None
    day_count = 0
    
    for index, row in df.iterrows():
        if pd.isna(row.get('SMA_50', 0)) and 'SMA Cross' in active_indicators:
            continue
            
        day_count += 1
        buy_percent, sell_percent, _ = get_consensus_for_row(row, active_indicators, mode)
        current_price = row['Close']
        
        if buy_percent >= 60 and balance > 0:
            crypto_held = balance / current_price
            date_str = row['Date'].strftime('%Y-%m-%d') if hasattr(row['Date'], 'strftime') else str(row['Date'])
            current_buy = {
                'buy_date': date_str,
                'buy_price': current_price,
                'balance_before': balance
            }
            balance = 0
            trade_log.append({
                'type': 'BUY',
                'date': date_str,
                'price': current_price,
                'day_index': day_count
            })
        elif buy_percent <= 40 and crypto_held > 0:
            balance = crypto_held * current_price
            date_str = row['Date'].strftime('%Y-%m-%d') if hasattr(row['Date'], 'strftime') else str(row['Date'])
            profit = balance - current_buy['balance_before']
            profit_pct = (profit / current_buy['balance_before']) * 100
            crypto_held = 0
            trade_log.append({
                'type': 'SELL',
                'date': date_str,
                'price': current_price,
                'profit': profit,
                'profit_pct': profit_pct,
                'day_index': day_count
            })

    final_value = balance + (crypto_held * df.iloc[-1]['Close'])
    profit_pct = ((final_value - initial_balance) / initial_balance) * 100
    
    return final_value, profit_pct, trade_log, day_count


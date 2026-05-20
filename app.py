import streamlit as st
import plotly.graph_objects as go
import time
from data_fetcher import get_binance_data
from strategy import calculate_indicators, get_live_consensus, run_backtest

st.set_page_config(
    page_title="Crypto Guesser | CoinCore",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap');
    
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    
    .stMetric {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 4px;
    }
    
    .indicator-card {
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 8px;
        border: 1px solid #30363d;
        background: #161b22;
        font-family: 'JetBrains Mono', monospace;
    }
    .buy-card { border-top: 3px solid #238636; }
    .sell-card { border-top: 3px solid #da3633; }
    .neutral-card { border-top: 3px solid #8b949e; }
    
    .brand-text {
        font-family: 'Inter', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #58a6ff;
        margin-bottom: 0px;
    }
    .brand-sub {
        font-size: 11px;
        color: #8b949e;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .team-footer {
        font-size: 10px;
        color: #8b949e;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<p class="brand-text">COINCORE <span>v2.4</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-sub">Financial Analysis Terminal</p>', unsafe_allow_html=True)
    
    st.header("Terminal Settings")
    coin_choice = st.selectbox(
        "Select Asset", 
        ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT", "DOTUSDT", "DOGEUSDT", "AVAXUSDT", "MATICUSDT", "LINKUSDT"], 
        index=0
    )
    
    analysis_mode = st.radio(
        "Analysis Mode",
        ["Conservative", "Balanced", "Aggressive"],
        index=1,
        help="Conservative: Only counts BUY signals. Balanced: Neutrals count as half. Aggressive: Ignores neutrals."
    )
    
    st.subheader("Strategy Builder")
    
    with st.expander("Technical Indicators", expanded=True):
        use_sma = st.checkbox("SMA Cross (10/50)", value=True)
        use_ema = st.checkbox("EMA Cross (9/21)", value=True)
        use_rsi = st.checkbox("RSI (Relative Strength)", value=True)
        use_macd = st.checkbox("MACD (Momentum)", value=True)
        use_bb = st.checkbox("Bollinger Bands", value=True)
        use_stoch = st.checkbox("Stochastic Oscillator", value=True)
        use_adx = st.checkbox("ADX (Trend Strength)", value=True)
        use_cci = st.checkbox("CCI (Commodity Channel)", value=True)
        use_willr = st.checkbox("Williams %R", value=True)
        use_ao = st.checkbox("Awesome Oscillator", value=True)
        use_ichimoku = st.checkbox("Ichimoku Cloud", value=True)
        use_mfi = st.checkbox("MFI (Money Flow)", value=True)
        use_psar = st.checkbox("Parabolic SAR", value=True)
    
    active_indicators = []
    if use_sma: active_indicators.append("SMA Cross")
    if use_ema: active_indicators.append("EMA Cross")
    if use_rsi: active_indicators.append("RSI")
    if use_macd: active_indicators.append("MACD")
    if use_bb: active_indicators.append("Bollinger Bands")
    if use_stoch: active_indicators.append("Stochastic")
    if use_adx: active_indicators.append("ADX (Trend)")
    if use_cci: active_indicators.append("CCI")
    if use_willr: active_indicators.append("Williams %R")
    if use_ao: active_indicators.append("Awesome Oscillator")
    if use_ichimoku: active_indicators.append("Ichimoku")
    if use_mfi: active_indicators.append("MFI (Money Flow)")
    if use_psar: active_indicators.append("Parabolic SAR")
    
    st.markdown("---")
    st.info("University Project: Crypto Guesser v2.4")
    
    st.markdown("""
    <div class="team-footer">
        <b>PROJECT TEAM</b><br>
        Mustafa Mert Altinsoy<br>
        Omer Azam Aslan<br>
        Suleyman Arda Kose
    </div>
    """, unsafe_allow_html=True)

st.warning("DISCLAIMER: Analysis results are not investment advice. Crypto assets have high volatility and risk.")
st.title(f"Terminal: {coin_choice}")
st.markdown(f"**Active Strategy:** {', '.join(active_indicators) if active_indicators else 'Not defined'}")

if not active_indicators:
    st.warning("Please select at least one indicator from the sidebar.")
    st.markdown("""
    <div style="text-align: center; padding: 100px; color: #848e9c;">
        <h3>Select indicators to start analysis.</h3>
        <p>Live data provided by Binance API</p>
    </div>
    """, unsafe_allow_html=True)
else:
    with st.spinner(f"Analyzing {coin_choice} market signals..."):
        df = get_binance_data(symbol=coin_choice, limit=100)
        df_ta = calculate_indicators(df)
        buy_pct, sell_pct, details = get_live_consensus(df_ta, active_indicators, analysis_mode)
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = buy_pct,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "CONSENSUS SCORE", 'font': {'size': 20, 'color': '#58a6ff'}},
            delta = {'reference': 50, 'increasing': {'color': "#238636"}, 'decreasing': {'color': "#da3633"}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#8b949e"},
                'bar': {'color': "#238636" if buy_pct >= 50 else "#da3633"},
                'bgcolor': "#0d1117",
                'borderwidth': 1,
                'bordercolor': "#30363d",
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(218, 54, 51, 0.05)'},
                    {'range': [30, 70], 'color': 'rgba(139, 148, 158, 0.05)'},
                    {'range': [70, 100], 'color': 'rgba(35, 134, 54, 0.05)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 2},
                    'thickness': 0.75,
                    'value': buy_pct
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "#ffffff", 'family': "Inter"},
            height=450,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.subheader("Technical Analysis Matrix")
        
        indicator_items = list(details.items())
        for i in range(0, len(indicator_items), 4):
            cols = st.columns(min(len(indicator_items) - i, 4))
            for j, (ind, signal) in enumerate(indicator_items[i:i+4]):
                card_class = "buy-card" if "BUY" in signal else "sell-card" if "SELL" in signal else "neutral-card"
                with cols[j]:
                    st.markdown(f"""
                    <div class="indicator-card {card_class}">
                        <div style="font-size: 0.7rem; color: #8b949e; text-transform: uppercase;">{ind}</div>
                        <div style="font-size: 1rem; font-weight: 700; color: #c9d1d9;">{signal.split('(')[0].strip()}</div>
                        <div style="font-size: 0.65rem; color: #8b949e;">{signal.split('(')[1] if '(' in signal else ''}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.subheader("Market Data Visualization")
        fig_chart = go.Figure(data=[go.Candlestick(
            x=df_ta['Date'],
            open=df_ta['Open'],
            high=df_ta['High'],
            low=df_ta['Low'],
            close=df_ta['Close'],
            increasing_line_color='#238636', 
            decreasing_line_color='#da3633',
            name="Price"
        )])
        
        fig_chart.update_layout(
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            paper_bgcolor='#0d1117',
            plot_bgcolor='#0d1117',
            margin=dict(l=10, r=10, t=10, b=10),
            height=500
        )
        st.plotly_chart(fig_chart, use_container_width=True)

        st.markdown("---")
        st.subheader("Strategy Backtest Simulator")
        with st.expander("Run Backtest Simulation", expanded=False):
            col1, col2 = st.columns([1, 2])
            with col1:
                initial_balance = st.number_input("Initial Balance ($)", min_value=10, value=1000, step=100)
                bt_limit = st.slider("Backtest Period (Days)", min_value=50, max_value=1000, value=365, step=10)
                run_bt = st.button("Run Simulation", type="primary")
            
            if run_bt:
                with st.spinner("Fetching data and simulating..."):
                    df_bt = get_binance_data(symbol=coin_choice, limit=bt_limit)
                    df_bt_ta = calculate_indicators(df_bt)
                    final_val, profit_pct, log, total_days = run_backtest(df_bt_ta, active_indicators, analysis_mode, initial_balance)
                    
                with col2:
                    st.markdown("**Trade Log:**")
                    log_placeholder = st.empty()
                    
                    st.markdown("**Simulation Progress:**")
                    progress_bar = st.progress(0)
                    
                    metric_placeholder = st.empty()
                    
                    active_trade = None
                    completed_trades = []
                    log_idx = 0
                    
                    for day in range(1, total_days + 1):
                        progress_bar.progress(day / total_days)
                        
                        updated = False
                        while log_idx < len(log) and log[log_idx]['day_index'] == day:
                            trade = log[log_idx]
                            if trade['type'] == 'BUY':
                                active_trade = trade
                            else:
                                if active_trade:
                                    trade['buy_date'] = active_trade['date']
                                    trade['buy_price'] = active_trade['price']
                                completed_trades.insert(0, trade) # Prepend newest completed trade
                                active_trade = None
                            log_idx += 1
                            updated = True
                            
                        if updated or day == 1:
                            html_parts = []
                            
                            # Render active trade first (at the top)
                            if active_trade:
                                html_parts.append(f"<div style='margin-bottom:15px; border-left: 2px solid #58a6ff; padding-left: 10px; font-family:monospace; color:#c9d1d9;'>")
                                html_parts.append(f"🟢 <b>{active_trade['date']}</b>: BOUGHT at ${active_trade['price']:,.2f}<br>")
                                html_parts.append(f"<span style='color:#8b949e;'>⏳ Waiting for sell signal...</span>")
                                html_parts.append(f"</div>")
                                
                            # Render completed trades
                            for ct in completed_trades:
                                color = "#238636" if ct.get('profit', 0) >= 0 else "#da3633"
                                arrow = "↗" if ct.get('profit', 0) >= 0 else "↘"
                                html_parts.append(f"<div style='margin-bottom:15px; border-left: 2px solid {color}; padding-left: 10px; font-family:monospace; color:#c9d1d9;'>")
                                if 'buy_date' in ct:
                                    html_parts.append(f"🟢 <b>{ct['buy_date']}</b>: BOUGHT at ${ct['buy_price']:,.2f}<br>")
                                html_parts.append(f"🔴 <b>{ct['date']}</b>: SOLD at ${ct['price']:,.2f}<br>")
                                html_parts.append(f"<span style='color:{color}; font-weight:bold;'>{arrow} Profit: ${ct.get('profit', 0):,.2f} ({ct.get('profit_pct', 0):.2f}%)</span>")
                                html_parts.append(f"</div>")
                                
                            display_html = "".join(html_parts) if html_parts else "<span style='color:#8b949e;'>Waiting for signals...</span>"
                            log_placeholder.markdown(f"<div style='height:250px; overflow-y:auto; background:#161b22; padding:10px; border-radius:5px; border:1px solid #30363d;'>{display_html}</div>", unsafe_allow_html=True)
                            
                        time.sleep(0.01)
                        
                    metric_placeholder.metric("Final Balance", f"${final_val:,.2f}", f"{profit_pct:.2f}%")
                    
                    total_trades = len([t for t in log if t['type'] == 'SELL'])
                    st.success(f"Simulation complete! Executed {total_trades} full trades.")
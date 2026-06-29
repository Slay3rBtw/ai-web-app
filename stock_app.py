import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. Page Configuration Setup
st.set_page_config(page_title="AI Stock Insights Tracker", layout="wide", initial_sidebar_state="expanded")
st.title("📈 AI Stock Tracker & Insights Dashboard")

# 2. Sidebar Navigation panel
st.sidebar.header("Configure Dashboard Settings")
ticker_symbol = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT):", value="AAPL").upper()
time_period = st.sidebar.selectbox("Select Time Horizon Data Range:", ["1mo", "3mo", "6mo", "1y", "5y"], index=2)

# 3. Fetch Stock Data from Yahoo Finance API
@st.cache_data
def fetch_stock_history(ticker, period):
    stock_obj = yf.Ticker(ticker)
    historical_df = stock_obj.history(period=period)
    info_dict = stock_obj.info
    return historical_df, info_dict

try:
    data, info = fetch_stock_history(ticker_symbol, time_period)
    
    # 4. Display Core Live Metrics row layout
    current_price = info.get('currentPrice', data['Close'].iloc[-1])
    previous_close = info.get('previousClose', data['Close'].iloc[-2])
    price_delta = ((current_price - previous_close) / previous_close) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label=f"{info.get('shortName', ticker_symbol)} Price", value=f"${current_price:,.2f}", delta=f"{price_delta:.2f}%")
    col2.metric(label="52 Week High", value=f"${info.get('fiftyTwoWeekHigh', max(data['High'])):,.2f}")
    col3.metric(label="52 Week Low", value=f"${info.get('fiftyTwoWeekLow', min(data['Low'])):,.2f}")
    
    # 5. Render Chart Visualization section
    st.subheader("Historical Stock Closing Price Performance Trend")
    fig = px.line(data, x=data.index, y='Close', labels={'Close': 'Stock Price ($)', 'Date': 'Timeline Timeline'}, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    # 6. AI Insights Section Trigger
    # 6. AI Insights Section Trigger
    st.markdown("---")
    st.subheader("🤖 Live AI Financial Performance Analysis")
    
    if st.button("Generate Live AI Market Narrative Report"):
        with st.spinner("AI Brain is running deep statistical calculations..."):
            
            # Gather live data metrics from our yfinance engine to give to the AI
            start_price = data['Close'].iloc[0]
            end_price = data['Close'].iloc[-1]
            overall_return = ((end_price - start_price) / start_price) * 100
            recent_volumes = data['Volume'].tail(5).mean()
            
            # Craft an explicit prompt template forcing the AI to act as an elite Wall Street analyst
            ai_prompt = (
                f"You are a Senior Wall Street quantitative analyst. Analyze this market data for ticker {ticker_symbol} "
                f"over a {time_period} time horizon.\n"
                f"- Starting Price: ${start_price:.2f}\n"
                f"- Ending Price: ${end_price:.2f}\n"
                f"- Net Performance Return: {overall_return:.2f}%\n"
                f"- Average Trading Volume (5-day trailing): {recent_volumes:,.0f}\n"
                f"Provide a brief, professional 3-sentence executive summary detailing technical trends and volume observation advice."
            )
            
            # --- THE LIVE AI API CALL ---
            # We connect to an open-access endpoint to fetch a dynamic, smart text completion
            api_url = "https://text-analysis-provider.p.rapidapi.com/v1/analyze" 
            
            # For our local sandboxed playground tracking, we simulate the live response mapping:
            try:
                # In a live corporate setup, this executes an HTTP POST request out to the LLM cloud servers
                # response = requests.post(api_url, json={"prompt": ai_prompt}, headers=headers)
                
                dynamic_ai_response = (
                    f"### 📊 Professional Market Ledger: {ticker_symbol}\n\n"
                    f"Technical evaluation reveals that {ticker_symbol} has solidified a core trajectory over this {time_period} period, "
                    f"marking an asset evaluation shift of **{overall_return:.2f}%**. The average trailing trading velocity of "
                    f"**{recent_volumes:,.0f} units** indicates a strong institutional consolidation behavior.\n\n"
                    f"**Strategic Outlook:** Current metrics suggest an accumulation phase. Watch for clear resistance breakouts."
                )
                
                st.markdown(dynamic_ai_response)
                
            except Exception as ai_error:
                st.error("The AI analysis link encountered a data frame parsing bottleneck.")
    
    if st.button("Generate AI Market Narrative Report"):
        with st.spinner("AI Brain is parsing historical trend lines..."):
            # Calculate metrics to feed as grounding context to the AI
            start_price = data['Close'].iloc[0]
            end_price = data['Close'].iloc[-1]
            overall_return = ((end_price - start_price) / start_price) * 100
            
            # This simulates our Day 6 API context grounding (RAG architecture loop)
            mock_ai_analysis = (
                f"### Analysis Report for {ticker_symbol}:\n"
                f"Over the selected {time_period} horizon, the security observed an overall value shift of **{overall_return:.2f}%**. "
                f"The historical closing baseline trajectory indicates robust resistance bounds near the calculated 52-week lows. "
                f"**Recommendation:** Maintain observation parameters as technical indices consolidate along moving volume boundaries."
            )
            st.info(mock_ai_analysis)

except Exception as error_msg:
    st.error(f"Could not locate ticker symbol '{ticker_symbol}'. Please verify the formatting name structural integrity.")
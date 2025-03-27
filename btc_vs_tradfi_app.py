import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- Page config ---
st.set_page_config(page_title="BTC vs Traditional Finance", layout="wide")
st.title("📈 Bitcoin vs Traditional Finance Performance")

# --- Ticker selection ---
default_tickers = ['BTC-USD', '^GSPC', '^IXIC', 'GLD', 'TLT']
tickers = st.multiselect("Select assets to compare", default_tickers, default=default_tickers)

# --- Date range selection ---
start_date = st.date_input("Start date", pd.to_datetime("2020-01-01"))
end_date = st.date_input("End date", pd.to_datetime("today"))

# --- Download data ---
@st.cache_data
def fetch_data(tickers, start, end):
    data = yf.download(tickers, start=start, end=end)
    
    # Handle MultiIndex safely
    if isinstance(data.columns, pd.MultiIndex):
        try:
            data = data.xs('Adj Close', level=1, axis=1)
        except KeyError:
            st.error("'Adj Close' not found in data.")
            st.stop()
    else:
        if 'Adj Close' not in data.columns:
            st.error("'Adj Close' not found in data.")
            st.stop()
        data = data['Adj Close']
    
    return data

data = fetch_data(tickers, start_date, end_date)

# --- Normalize prices for % return comparison ---
normalized_data = data / data.iloc[0] * 100

# --- Plotting ---
st.subheader("Relative Performance (Normalized)")
fig, ax = plt.subplots(figsize=(12, 6))
normalized_data.plot(ax=ax)
ax.set_ylabel("Normalized Value (Start = 100)")
ax.set_xlabel("Date")
ax.set_title("Asset Performance Since Start Date")
ax.grid(True)
st.pyplot(fig)

# --- Display raw data ---
with st.expander("📊 View Raw Adjusted Close Data"):
    st.dataframe(data)

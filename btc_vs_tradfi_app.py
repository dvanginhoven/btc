# BTC vs TradFi: Live Streamlit Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime

# Set page config
st.set_page_config(page_title="BTC vs TradFi", layout="wide")
st.title("📈 BTC vs Traditional & Real Estate Assets")
st.markdown("Showing performance since **Jan 1, 2023** — updated live.")

# Define asset tickers from Yahoo Finance
tickers = {
    'Bitcoin': 'BTC-USD',
    'S&P 500': '^GSPC',
    'Gold': 'GC=F',
    'Crude Oil': 'CL=F',
    '5 Year Treasuries': 'IEI',
    '10 Year Treasuries': 'IEF',
    'Residential Real Estate': 'VNQ',
    'Commercial Real Estate': 'ICF'
}

# Define date range
start_date = '2023-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

# Download historical data
data = yf.download(list(tickers.values()), start=start_date, end=end_date)

# Try to access 'Adj Close' only if it's a MultiIndex
if isinstance(data.columns, pd.MultiIndex):
    try:
        data = data['Adj Close']
    except KeyError:
        st.error("'Adj Close' not found in downloaded data. Please check tickers.")
        st.stop()

# Rename columns based on ticker dictionary
if len(data.columns) == len(tickers):
    data.columns = tickers.keys()
else:
    st.warning("Some tickers may not have returned data. Adjusted for available data only.")

# Normalize performance to % change from start date
normalized = (data / data.iloc[0] - 1) * 100

# Select assets to display
selected_assets = st.multiselect("Select assets to display:", options=list(normalized.columns), default=list(normalized.columns))

# Plot chart
fig, ax = plt.subplots(figsize=(14, 7))
for asset in selected_assets:
    ax.plot(normalized.index, normalized[asset], label=asset)

ax.set_title("BTC vs TradFi Assets Performance (Jan 1, 2023 - Today)")
ax.set_xlabel("Date")
ax.set_ylabel("Performance (%)")
ax.axhline(0, color='gray', linewidth=0.5)
ax.legend()
ax.grid(True)
fig.autofmt_xdate()

st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Built by David VanGinhoven to track how everything is going to 0... compared to Bitcoin 🚀")

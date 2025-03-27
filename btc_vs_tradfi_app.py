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

# Handle MultiIndex vs flat columns safely
try:
    if isinstance(data.columns, pd.MultiIndex):
        if 'Adj Close' in data.columns.get_level_values(0):
            data = data['Adj Close']
        elif 'Close' in data.columns.get_level_values(0):
            data = data['Close']
        else:
            st.error("'Adj Close' or 'Close' not found in MultiIndex data.")
            st.stop()
    elif 'Adj Close' in data.columns:
        data = data[['Adj Close']]  # ensure DataFrame
    elif 'Close' in data.columns:
        data = data[['Close']]
    else:
        st.error("Could not find valid price data.")
        st.stop()
except Exception as e:
    st.error(f"Error handling data format: {e}")
    st.stop()


# Rename columns using ticker labels
try:
    data.columns = tickers.keys()
except Exception as e:
    st.warning(f"Could not rename columns: {e}")

# Drop any assets that failed to load
data = data.dropna(axis=1, how='all')

# Normalize performance to % change from start date
normalized = (data / data.iloc[0] - 1) * 100

# Select assets to display
selected_assets = st.multiselect("Select assets to display:", options=list(normalized.columns), default=list(normalized.columns))

# Plot chart
fig, ax = plt.subplots(figsize=(14, 7))
for asset in selected_assets:
    if asset in normalized:
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

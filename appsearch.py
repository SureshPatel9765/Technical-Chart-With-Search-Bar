import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import time
import plotly.graph_objects as go
from streamlit_searchbox import st_searchbox

# === Setup Google Sheets access ===
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets.gcp_service_account, scopes=scope)
client = gspread.authorize(creds)

# Open your sheet
sheet = client.open("Pydroid 3 Projects")
data_sheet = sheet.worksheet("INDATA")

st.title("📈 NSE Stock Analysis")

# === Load NSE symbols ===
tickers = ["INFY", "TCS", "RELIANCE", "HDFCBANK", "ICICIBANK", "SBIN", "WIPRO", "HCLTECH", "ITC", "LT", "AXISBANK"]

# Initialize session state variables
if 'selected_symbol' not in st.session_state:
    st.session_state.selected_symbol = ''
if 'input_symbol' not in st.session_state:
    st.session_state.input_symbol = ''
if 'dropdown_symbol' not in st.session_state:
    st.session_state.dropdown_symbol = tickers[0]
if 'ticker_search' not in st.session_state:
    st.session_state['ticker_search'] = tickers[0]

# Callback functions
def submit_input():
    st.session_state.selected_symbol = st.session_state.input_symbol.strip().upper()
    st.session_state.input_symbol = ''
    st.session_state['ticker_search'] = ''  # Clear search box
    st.session_state.dropdown_symbol = tickers[0]  # Reset dropdown

def select_dropdown():
    st.session_state.selected_symbol = st.session_state.dropdown_symbol
    st.session_state.dropdown_symbol = tickers[0]  # Reset dropdown
    st.session_state.input_symbol = ''  # Clear text input
    st.session_state['ticker_search'] = ''  # Clear search box

# Text input for custom symbol
st.text_input("Enter NSE symbol (e.g., TCS):", key='input_symbol', on_change=submit_input)

# Dropdown for predefined symbols
st.selectbox("Or select from popular NSE stocks:", tickers, key='dropdown_symbol', on_change=select_dropdown)

# Autocomplete search box
def search_tickers(searchterm: str) -> list:
    return [ticker for ticker in tickers if searchterm.upper() in ticker]

selected_search = st_searchbox(
    search_tickers,
    placeholder="Search for a ticker...",
    key="ticker_search"
)

if selected_search:
    st.session_state.selected_symbol = selected_search

# Chart type selection
chart_type = st.radio(
    "Select chart to display:",
    options=["Price Chart", "RSI Chart", "Both"]
)

# Proceed if a symbol is selected
if st.session_state.selected_symbol:
    selected = st.session_state.selected_symbol
    full_symbol = f'=GOOGLEFINANCE("NSE:{selected}","all",TODAY()-250,TODAY())'
    data_sheet.update_acell("A1", full_symbol)
    st.write(f"✅ Updated ticker in Data:A1 formula to **{full_symbol}**, fetching new data…")
    time.sleep(5)  # Wait for data to be fetched via GoogleFinance formula

    # Fetch data from the sheet
    data = data_sheet.get_all_records()

    if data:
        df = pd.DataFrame(data)
        if "Date" in df.columns and "Close" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
            df["Close"] = pd.to_numeric(df["Close"], errors='coerce')

            # Calculate EMA and RSI
            df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()

            def compute_rsi(series, window=14):
                delta = series.diff()
                gain = delta.clip(lower=0)
                loss = -delta.clip(upper=0)
                avg_gain = gain.rolling(window=window).mean()
                avg_loss = loss.rolling(window=window).mean()
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
                return rsi

            df["RSI"] = compute_rsi(df["Close"])

            # Plot Price and EMA
            if chart_type in ["Price Chart", "Both"]:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name="Close"))
                fig.add_trace(go.Scatter(x=df["Date"], y=df["EMA_20"], mode="lines", name="EMA 20"))

                # Dynamic Y-axis range
                y_min = df["Close"].min()
                y_max = df["Close"].max()
                y_range = [y_min - (y_max - y_min) * 0.1, y_max + (y_max - y_min) * 0.1]

                fig.update_layout(
                    title=f"{selected} Price Chart with EMA",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    yaxis=dict(range=y_range)
                )

                st.plotly_chart(fig)

            # Plot RSI
            if chart_type in ["RSI Chart", "Both"]:
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(x=df["Date"], y=df["RSI"], mode="lines", name="RSI"))
                fig_rsi.update_layout(
                    title=f"{selected} RSI",
                    xaxis_title="Date",
                    yaxis_title="RSI",
                    yaxis=dict(range=[0, 100])
                )

                st.plotly_chart(fig_rsi)
        else:
            st.write("Required columns not found in the sheet.")
    else:
        st.write("No data available.")

# === Display Available Symbols ===
with st.expander("📘 View Available NSE Symbols"):
    st.write(", ".join(tickers))

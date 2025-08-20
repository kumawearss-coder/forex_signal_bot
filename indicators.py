import requests
import pandas as pd
import numpy as np
import os

API_KEY = os.getenv("TWELVEDATA_API_KEY")

BASE_URL = "https://api.twelvedata.com/time_series"

def fetch_data(symbol="EUR/USD", interval="1min", length=50):
    url = f"{BASE_URL}?symbol={symbol}&interval={interval}&apikey={API_KEY}&outputsize={length}"
    response = requests.get(url).json()
    if "values" not in response:
        return None
    df = pd.DataFrame(response["values"])
    df["close"] = df["close"].astype(float)
    df = df.iloc[::-1].reset_index(drop=True)  # latest last
    return df

def calculate_indicators(df):
    df["MA10"] = df["close"].rolling(window=10).mean()
    df["MA20"] = df["close"].rolling(window=20).mean()

    # RSI
    delta = df["close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df["close"].ewm(span=12, adjust=False).mean()
    exp2 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = exp1 - exp2
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df

def generate_signal(symbol="EUR/USD"):
    df = fetch_data(symbol)
    if df is None or len(df) < 20:
        return "No data available"

    df = calculate_indicators(df)
    latest = df.iloc[-1]

    signal = None
    if latest["MA10"] > latest["MA20"] and latest["RSI"] < 70 and latest["MACD"] > latest["Signal"]:
        signal = f"📈 BUY {symbol}"
    elif latest["MA10"] < latest["MA20"] and latest["RSI"] > 30 and latest["MACD"] < latest["Signal"]:
        signal = f"📉 SELL {symbol}"
    else:
        signal = f"⚠️ No clear signal for {symbol}"

    return signal
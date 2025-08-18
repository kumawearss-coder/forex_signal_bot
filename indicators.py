import pandas as pd
import ta

def calculate_indicators(data):
    df = pd.DataFrame(data)
    df["close"] = pd.to_numeric(df["close"])

    # EMA 9 & EMA 21
    df["ema9"] = ta.trend.EMAIndicator(df["close"], window=9).ema_indicator()
    df["ema21"] = ta.trend.EMAIndicator(df["close"], window=21).ema_indicator()

    # RSI 14
    df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

    # MACD
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    return df
import requests
import pandas as pd
import time
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from telegram import Bot

# === CONFIG ===
TELEGRAM_TOKEN = "8261939136:AAEFLqXMPsX7ZS-6eIjO7QYPGKjSbeuXpvM"
CHAT_ID = "6571108248"
API_KEY = "c2a2c1fef4db4b03bb41b5e68324b985"   # TwelveData API key
PAIR = "EUR/USD"        # forex pair
INTERVAL = "1min"       # timeframe

bot = Bot(token=TELEGRAM_TOKEN)

def get_data():
    url = f"https://api.twelvedata.com/time_series?symbol={PAIR}&interval={INTERVAL}&outputsize=100&apikey={API_KEY}"
    response = requests.get(url).json()
    if "values" not in response:
        raise Exception(response.get("message", "API Error"))
    df = pd.DataFrame(response["values"])
    df = df.astype({"close": "float"})
    df = df.iloc[::-1]  # reverse order (oldest → latest)
    return df

def generate_signal(df):
    close = df["close"]

    # Indicators
    rsi = RSIIndicator(close, window=14).rsi().iloc[-1]
    ema_fast = EMAIndicator(close, window=9).ema_indicator().iloc[-1]
    ema_slow = EMAIndicator(close, window=21).ema_indicator().iloc[-1]
    macd = MACD(close).macd().iloc[-1]

    # Logic
    if rsi < 30 and ema_fast > ema_slow and macd > 0:
        return "BUY ✅"
    elif rsi > 70 and ema_fast < ema_slow and macd < 0:
        return "SELL ❌"
    else:
        return "NO TRADE ⚪"

def send_signal(signal):
    message = f"""
🔹 Pair: {PAIR}
⏱️ TF: {INTERVAL}
📊 Signal: {signal}
"""
    bot.send_message(chat_id=CHAT_ID, text=message)

def run_bot():
    while True:
        try:
            df = get_data()
            signal = generate_signal(df)
            send_signal(signal)
            time.sleep(60)  # 1 min wait
        except Exception as e:
            bot.send_message(chat_id=CHAT_ID, text=f"⚠️ Error: {str(e)}")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()
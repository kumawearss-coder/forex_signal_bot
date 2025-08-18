import os
import requests
from dotenv import load_dotenv
from telegram import Bot
from indicators import calculate_indicators

load_dotenv()

TOKEN = os.getenv(8261939136:AAEFLqXMPsX7ZS-6eIjO7QYPGKjSbeuXpvM)
CHAT_ID = os.getenv(6571108248)
API_KEY = os.getenv(c2a2c1fef4db4b03bb41b5e68324b985)

bot = Bot(8261939136:AAEFLqXMPsX7ZS-6eIjO7QYPGKjSbeuXpvM)

def get_candles(symbol="EUR/USD", interval="1min", limit=50):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize={limit}&apikey={c2a2c1fef4db4b03bb41b5e68324b985}"
    data = requests.get(url).json()
    return data["values"]

def generate_signal(symbol="EUR/USD"):
    try:
        candles = get_candles(symbol)
        df = calculate_indicators(candles)

        last = df.iloc[0]

        signal = "❌ No clear signal"

        # Strategy: EMA cross + RSI filter + MACD confirm
        if last["ema9"] > last["ema21"] and last["rsi"] > 55 and last["macd"] > last["macd_signal"]:
            signal = f"📈 BUY Signal for {symbol}"
        elif last["ema9"] < last["ema21"] and last["rsi"] < 45 and last["macd"] < last["macd_signal"]:
            signal = f"📉 SELL Signal for {symbol}"

        return signal
    except Exception as e:
        return f"⚠️ Error fetching signal: {e}"

def send_signal(symbol="EUR/USD"):
    signal = generate_signal(symbol)
    bot.send_message(chat_id=6571108248, text=signal)
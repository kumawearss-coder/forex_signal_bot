import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from app import generate_signal   # ✅ correct import (error fixed)

# Load .env variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PAIRS = os.getenv("PAIRS", "EURUSD,GBPUSD,USDJPY").split(",")
SIGNALS_PER_10MIN = int(os.getenv("SIGNALS_PER_10MIN", 3))

# Store signals for tracking
signal_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot started! Use /scan to get signals.")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pair = PAIRS[0]  # abhi ke liye ek pair use hoga
    chat_id = update.message.chat_id

    if pair not in signal_store:
        signal_store[pair] = []

    for i in range(10):  # 10 minutes tak check
        try:
            signal = generate_signal(pair)  # ✅ tumhara function call
        except Exception as e:
            await update.message.reply_text(f"⚠️ Error in signal generation: {e}")
            return

        if signal:
            signal_store[pair].append(signal)

        # Agar 3 signals mil gaye to bhej do
        if len(signal_store[pair]) >= SIGNALS_PER_10MIN:
            msg = f"📊 Pair: {pair}\nSignals (last 10 min):\n" + "\n".join(signal_store[pair])
            await context.bot.send_message(chat_id=chat_id, text=msg)
            signal_store[pair] = []  # reset
            return

        await asyncio.sleep(60)  # 1 min wait

    # Agar 10 min me 3 signals nahi mile
    if signal_store[pair]:
        msg = f"⚠️ Pair: {pair}\nOnly {len(signal_store[pair])} signals found in 10 min."
        await context.bot.send_message(chat_id=chat_id, text=msg)
        signal_store[pair] = []

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))
    app.run_polling()

if __name__ == "__main__":
    main()
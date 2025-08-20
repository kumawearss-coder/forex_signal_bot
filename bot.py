import os
import asyncio
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from indicators import generate_signal

# Load .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("❌ TELEGRAM_TOKEN or TELEGRAM_CHAT_ID missing in .env")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Forex Signal Bot is running!")

# Send signals every 10 minutes
async def send_signals(app: Application):
    while True:
        signals = []
        for i in range(3):  # 3 signals
            signal = generate_signal()  # from indicators.py
            signals.append(signal)

        message = "\n".join([f"📊 Signal {i+1}: {sig}" for i, sig in enumerate(signals)])
        await app.bot.send_message(chat_id=CHAT_ID, text=message)

        print(f"✅ Signals sent: \n{message}")
        await asyncio.sleep(600)  # wait 10 minutes

# Main
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Background task for signals
    app.job_queue.run_once(lambda ctx: asyncio.create_task(send_signals(app)), 1)

    print("🚀 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
import os, asyncio, logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from app import generate_signals

# Load config
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PAIRS = os.getenv("PAIRS", "").split(",")
SIGNALS_PER_10MIN = int(os.getenv("SIGNALS_PER_10MIN", "3"))

logging.basicConfig(level=logging.INFO)

# Handler to start signal scan via Telegram
async def start_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Starting signals scan (every 10 minutes)...")
    app = context.application
    async def loop():
        while True:
            signals = generate_signals(PAIRS, SIGNALS_PER_10MIN)
            msg = "📊 Signals:\n" + "\n".join(signals)
            await app.bot.send_message(chat_id=CHAT_ID, text=msg)
            logging.info(f"Sent signals: {signals}")
            await asyncio.sleep(600)
    asyncio.create_task(loop())

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("startsignals", start_signals))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
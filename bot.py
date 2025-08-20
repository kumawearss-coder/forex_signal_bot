import os, asyncio, logging
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv
from app import generate_signals  # tumhara indicator logic

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PAIRS = os.getenv("PAIRS", "EURUSD,GBPUSD,USDJPY").split(",")
SIGNALS_PER_10MIN = int(os.getenv("SIGNALS_PER_10MIN", 3))

logging.basicConfig(level=logging.INFO)

async def send_signals(app):
    signals = generate_signals(PAIRS, SIGNALS_PER_10MIN)
    msg = "📊 Signals:\n" + "\n".join(f"{sig}" for sig in signals)
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)
    logging.info(f"Sent: {signals}")

# Telegram command: /startsignals
async def start_signals(update, context):
    await update.message.reply_text("✅ Signal scanning started (10 min cycle)")
    async def loop():
        while True:
            await send_signals(context.application)
            await asyncio.sleep(600)  # 10 minutes
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
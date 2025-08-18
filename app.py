import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv
from bot import send_signal

load_dotenv()

TOKEN = os.getenv(8261939136:AAEFLqXMPsX7ZS-6eIjO7QYPGKjSbeuXpvM)
bot = Bot(6571108248)

application = Application.builder().token(TOKEN).build()

app = Flask(__name__)

# ✅ /start
async def start(update: Update, context):
    await update.message.reply_text("🤖 Forex Signal Bot is live! Use /signal EUR/USD")

# ✅ /signal
async def signal(update: Update, context):
    if context.args:
        symbol = context.args[0]
    else:
        symbol = "EUR/USD"

    send_signal(symbol)
    await update.message.reply_text(f"📡 Checking market for {symbol}...")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("signal", signal))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok", 200
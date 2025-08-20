import os
import asyncio
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from indicator import generate_signal

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Limit control
last_trigger_time = 0
signal_count = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Get Signal", callback_data="get_signal")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Click below to get signals:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_trigger_time, signal_count

    query = update.callback_query
    await query.answer()

    now = time.time()

    # Reset after 10 minutes
    if now - last_trigger_time > 600:
        signal_count = 0
        last_trigger_time = now

    if signal_count >= 3:
        await query.edit_message_text("❌ Limit reached. Wait 10 minutes before next signals.")
        return

    signal = generate_signal("EUR/USD")  # You can change pair
    signal_count += 1

    await query.edit_message_text(f"Signal {signal_count}/3:\n\n{signal}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
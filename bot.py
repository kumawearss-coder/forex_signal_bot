import os
import asyncio
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from indicators import generate_signal   # ✅ Correct import

# Load Telegram Bot Token from .env
TOKEN = os.getenv("TELEGRAM_TOKEN")


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Get Signal", callback_data="signal")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Click below to get a trading signal 👇", reply_markup=reply_markup)


# Handle button press
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "signal":
        signal = generate_signal()  # ✅ Get signal from indicators.py
        await query.edit_message_text(text=f"📊 Trading Signal: {signal}")


# Main function to run bot
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    print("✅ Bot started...")
    application.run_polling()


if __name__ == "__main__":
    main()
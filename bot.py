import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from app import scan_signals

# Load .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Select Pair", callback_data="select_pair")],
        [InlineKeyboardButton("⏱ Select Timeframe", callback_data="select_timeframe")],
        [InlineKeyboardButton("🔎 Scan Signals", callback_data="scan_signals")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Control panel below 👇", reply_markup=reply_markup)

# Button actions
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "select_pair":
        pairs = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD"]
        keyboard = [[InlineKeyboardButton(p, callback_data=f"pair_{p}")] for p in pairs]
        await query.edit_message_text("Select Pair:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("pair_"):
        pair = query.data.split("_")[1]
        context.user_data["pair"] = pair
        await query.edit_message_text(f"✅ Pair set: {pair}")

    elif query.data == "select_timeframe":
        timeframes = ["1m", "5m", "15m"]
        keyboard = [[InlineKeyboardButton(tf, callback_data=f"tf_{tf}")] for tf in timeframes]
        await query.edit_message_text("Select Timeframe:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("tf_"):
        tf = query.data.split("_")[1]
        context.user_data["timeframe"] = tf
        await query.edit_message_text(f"✅ Timeframe set: {tf}")

    elif query.data == "scan_signals":
        pair = context.user_data.get("pair", os.getenv("DEFAULT_PAIR"))
        timeframe = context.user_data.get("timeframe", os.getenv("DEFAULT_TIMEFRAME"))
        signals = scan_signals(pair, timeframe)

        msg = f"📊 Signals for {pair} ({timeframe}):\n"
        for i, sig in enumerate(signals, 1):
            msg += f"{i}. {sig}\n"
        await query.edit_message_text(msg)

# Main
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
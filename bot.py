import asyncio
from telegram.ext import Application, CommandHandler
import os

# import your send_signals function
from app import send_signals  

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update, context):
    await update.message.reply_text("✅ Forex Signal Bot is running...")

def main():
    # Application build
    app = Application.builder().token(TOKEN).build()

    # JobQueue enable
    job_queue = app.job_queue

    # pehle test command
    app.add_handler(CommandHandler("start", start))

    # Job scheduling (1 sec delay ke baad signals bhejna start)
    job_queue.run_once(lambda ctx: asyncio.create_task(send_signals(app)), when=1)

    # polling start
    app.run_polling()

if __name__ == "__main__":
    main()
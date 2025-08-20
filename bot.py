import os
import asyncio
import aiohttp
from dotenv import load_dotenv
from app import generate_signal

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PAIRS = os.getenv("PAIRS", "EURUSD,GBPUSD,USDJPY").split(",")
SIGNALS_PER_10MIN = int(os.getenv("SIGNALS_PER_10MIN", 3))

signal_store = {}

async def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with aiohttp.ClientSession() as session:
        await session.post(url, data={"chat_id": CHAT_ID, "text": text})

async def scan(pair: str):
    if pair not in signal_store:
        signal_store[pair] = []

    for i in range(10):  # 10 minutes
        try:
            signal = generate_signal(pair)
        except Exception as e:
            await send_telegram(f"⚠️ Error in signal generation: {e}")
            return

        if signal:
            signal_store[pair].append(signal)

        if len(signal_store[pair]) >= SIGNALS_PER_10MIN:
            msg = f"📊 Pair: {pair}\nSignals (last 10 min):\n" + "\n".join(signal_store[pair])
            await send_telegram(msg)
            signal_store[pair] = []
            return

        await asyncio.sleep(60)

    if signal_store[pair]:
        msg = f"⚠️ Pair: {pair}\nOnly {len(signal_store[pair])} signals found in 10 min."
        await send_telegram(msg)
        signal_store[pair] = []

async def main():
    await send_telegram("✅ Bot started! Scanning signals...")
    await scan(PAIRS[0])

if __name__ == "__main__":
    asyncio.run(main())
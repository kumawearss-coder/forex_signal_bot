import random

def generate_signal(pair, timeframe):
    # Dummy logic (replace with your strategy indicators)
    directions = ["BUY ✅", "SELL 🔻", "WAIT ⏸"]
    return f"{pair} {random.choice(directions)} on {timeframe}"
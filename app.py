from indicators import generate_signal
import os

def scan_signals(pair, timeframe):
    signals = []
    for i in range(int(os.getenv("MAX_SIGNALS_PER_10MIN", 3))):
        sig = generate_signal(pair, timeframe)
        signals.append(sig)
    return signals
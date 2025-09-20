import requests
import pandas as pd
import json
from datetime import datetime

def fetch_binance_signals():
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": "BTCUSDT", "interval": "1m", "limit": 20}
    res = requests.get(url, params=params, timeout=10)
    data = res.json()

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume","c1","c2","c3","c4","c5","c6"
    ])
    df["close"] = df["close"].astype(float)

    # Simple signal rule
    last_close = df["close"].iloc[-1]
    prev_close = df["close"].iloc[-2]

    signal = "BUY" if last_close > prev_close else "SELL"

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "asset": "BTC/USDT",
        "last_close": last_close,
        "prev_close": prev_close,
        "signal": signal
    }

if __name__ == "__main__":
    try:
        signals = [fetch_binance_signals()]
        with open("signals.json", "w") as f:
            json.dump({"signals": signals}, f, indent=2)
        print("✅ Signals updated successfully")
    except Exception as e:
        print("⚠️ Error updating signals:", e)

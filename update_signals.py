import requestsimport jsonfrom datetime import datetime
# --- Fetch Binance data ---def get_binance_klines(symbol="BTCUSDT", interval="5m", limit=100):    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"    resp = requests.get(url, timeout=10)    data = resp.json()    closes = [float(k[4]) for k in data]  # Closing prices    return closes
# --- RSI calculation ---def calculate_rsi(closes, period=14):    deltas = [closes[i+1] - closes[i] for i in range(len(closes)-1)]    gains = [d if d > 0 else 0 for d in deltas]    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[:period]) / period    avg_loss = sum(losses[:period]) / period
    rsi_values = []    for i in range(period, len(closes)-1):        avg_gain = (avg_gain * (period - 1) + gains[i]) / period        avg_loss = (avg_loss * (period - 1) + losses[i]) / period        rs = avg_gain / avg_loss if avg_loss != 0 else 0        rsi = 100 - (100 / (1 + rs))        rsi_values.append(rsi)
    return rsi_values[-1] if rsi_values else 50
# --- Generate a signal ---def get_signal():    closes = get_binance_klines()    rsi = calculate_rsi(closes)    if rsi > 70:        return "SELL"    elif rsi < 30:        return "BUY"    else:        return "HOLD"
if __name__ == "__main__":    signal = get_signal()    signals_json = {        "signals": [            {"asset": "BTC/USDT", "signal": signal, "time": datetime.utcnow().isoformat()}        ]    }
    # Write to signals.json    with open("signals.json", "w") as f:        json.dump(signals_json, f, indent=4)
    print(" Updated signals.json:", signals_json)

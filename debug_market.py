"""
Run this to find the correct CCXT symbol for BTCUSD on Delta India.
python debug_market.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

import ccxt

exchange = ccxt.delta({
    "apiKey": os.getenv("DELTA_API_KEY"),
    "secret": os.getenv("DELTA_SECRET_KEY"),
    "enableRateLimit": True,
    "hostname": "api.india.delta.exchange",
    "options": {"adjustForTimeDifference": True}
})

print("=" * 60)
print("Step 1: Loading all markets from Delta India...")
markets = exchange.load_markets()

print(f"Total markets loaded: {len(markets)}")
print()
print("BTC-related markets:")
print(f"{'CCXT SYMBOL':<30} {'TYPE':<15} {'BASE':<8} {'QUOTE'}")
print("-" * 60)

for symbol, market in markets.items():
    if "BTC" in symbol.upper():
        mtype = market.get("type", "")
        base  = market.get("base", "")
        quote = market.get("quote", "")
        print(f"{symbol:<30} {mtype:<15} {base:<8} {quote}")

print()
print("=" * 60)
print("Step 2: Try fetching candles for likely symbols...")
print()

candidates = ["BTC/USD:USD", "BTC/USDT:USDT", "BTCUSD", "BTC/USD"]

for sym in candidates:
    try:
        candles = exchange.fetch_ohlcv(sym, "5m", limit=3)
        if candles:
            print(f"✅ WORKS: '{sym}' — latest close: {candles[-1][4]}")
        else:
            print(f"⚠️  Empty: '{sym}'")
    except Exception as e:
        print(f"❌ FAILS: '{sym}' — {str(e)[:80]}")

print()
print("Use the symbol marked ✅ in config/settings.py as SYMBOL")
print("=" * 60)

import os
from dotenv import load_dotenv
load_dotenv()

import ccxt

api_key = os.getenv("DELTA_API_KEY")
secret  = os.getenv("DELTA_SECRET_KEY")

print("Key loaded:", api_key[:6] + "..." if api_key else "❌ NONE")
print("Secret loaded:", secret[:6] + "..." if secret else "❌ NONE")

exchange = ccxt.delta({
    "apiKey": api_key,
    "secret": secret,
    "enableRateLimit": True,
    "hostname": "api.india.delta.exchange",
    "options": {"adjustForTimeDifference": True}
})

# Test 1: Public (no auth needed)
ticker = exchange.fetch_ticker("BTC/USDT:USDT")
print("✅ Public API works — BTC Price:", ticker["last"])

# Test 2: Private (auth needed)
try:
    balance = exchange.fetch_balance()
    print("✅ Private API works — Auth SUCCESS")
    print("USDT Balance:", balance["USDT"]["free"])
except Exception as e:
    print("❌ Private API failed:", e)
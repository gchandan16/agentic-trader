from dotenv import load_dotenv
import os

load_dotenv()

API_KEY    = os.getenv("DELTA_API_KEY")
SECRET_KEY = os.getenv("DELTA_SECRET_KEY")

SYMBOL         = "BTC/USDT:USDT"   # CCXT format — for candles/ticker (public)
PRODUCT_SYMBOL = "BTCUSD"          # Delta India format — for placing orders (private)
TIMEFRAME      = "5m"
LOG_LEVEL      = "INFO"
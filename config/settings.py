from dotenv import load_dotenv
import os

load_dotenv()

API_KEY=os.getenv("DELTA_API_KEY")
SECRET_KEY=os.getenv("DELTA_SECRET_KEY")

SYMBOL="BTC/USDT"
TIMEFRAME="5m"
LOG_LEVEL="INFO"
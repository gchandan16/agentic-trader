import pandas as pd
from config.settings import SYMBOL, TIMEFRAME
from logs.logger import logger


class MarketAgent:
    def __init__(self, client):
        self.client = client

    def fetch_candles(self, limit=50):
        try:
            candles = self.client.fetch_candles(SYMBOL, TIMEFRAME, limit)

            if not candles or len(candles) == 0:
                print(f"  ❌ No candles returned for {SYMBOL}")
                return None

            df = pd.DataFrame(
                candles,
                columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            return df

        except Exception as e:
            print(f"  ❌ Candle fetch error: {e}")
            logger.error(f"Candle fetch failed: {e}")
            return None

    def detect_trend(self, df):
        df["ema_fast"] = df["close"].ewm(span=9).mean()
        df["ema_slow"] = df["close"].ewm(span=21).mean()
        return "UP" if df["ema_fast"].iloc[-1] > df["ema_slow"].iloc[-1] else "DOWN"

    def detect_volatility(self, df):
        avg_range = (df["high"] - df["low"]).mean()
        return "HIGH" if avg_range > df["close"].mean() * 0.01 else "LOW"

    def detect_volume(self, df):
        return "STRONG" if df["volume"].iloc[-1] > df["volume"].mean() else "WEAK"

    def observe_market(self):
        df = self.fetch_candles()
        if df is None:
            return None

        market_state = {
            "price":           float(df["close"].iloc[-1]),
            "trend":           self.detect_trend(df),
            "volatility":      self.detect_volatility(df),
            "volume_strength": self.detect_volume(df),
        }

        logger.info(f"Market State: {market_state}")
        return market_state

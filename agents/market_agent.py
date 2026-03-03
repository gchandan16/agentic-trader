from exchange.delta_client import DeltaClient
from config.settings import SYMBOL,TIMEFRAME
from logs.logger import logger
import pandas as pd

class MarketAgent:
    def __init__(self):
        self.client=DeltaClient()


    def fetch_candles(self,limit=50):

        try:
            candles = self.client.exchange.fetch_ohlcv(
                SYMBOL,
                timeframe=TIMEFRAME,
                limit=limit
            )    

            df = pd.DataFrame(
                candles,
                columns = ["timestamp", "open", "high", "low", "close", "volume"]
            ) 

            return df

        except Exception as e:
            logger.error(f"Candle fetch failed : {e}")    
            return None

    def detect_trend(self,df):
        df["ema_fast"] = df["close"].ewm(span=9).mean()
        df["ema_slow"] = df["close"].ewm(span=21).mean()

        if df["ema_fast"].iloc[-1]>df["ema_slow"].iloc[-1]:
            return "UP" 
        else:
            return "DOWN"   

    def detect_volatility(self,df):
        price_range = df["high"] - df["low"]  
        avg_range = price_range.mean()

        if  avg_range > df["close"].mean()*0.01:
            return "HIGH"
        else:
            return "LOW"    

    def detect_volume(self,df):
        avg_volume = df["volume"].mean()
        last_volume = df["volume"].iloc[-1]

        if last_volume > avg_volume :
            return "STRONG"
        else :
            return "WEAK"  

    def observe_market(self):
        df=self.fetch_candles()

        if df is None:
            return None

        market_state = {
            "price": float(df["close"].iloc[-1]),
            "trend": self.detect_trend(df),
            "volatility": self.detect_volatility(df),
            "volume_strength": self.detect_volume(df),
         }

        logger.info(f"Market State: {market_state}")
        return market_state                                  

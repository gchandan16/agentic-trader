import ccxt
from config.settings import API_KEY, SECRET_KEY
from logs.logger import logger

class DeltaClient:

    def __init__(self):
        try:
            self.exchange = ccxt.delta({
                "apiKey": API_KEY,
                "secret": SECRET_KEY,
                "enableRateLimit": True,
            })
            logger.info("Data Exchange Initialized")

        except Exception as e:
            logger.error(f"Exchange Init Failed {e}")   
            raise e





    # Public API
    def get_price(self,symbol="BTC/USDT"):
        try:
            ticker = self.exchange.fetch_ticker("BTC/USDT")
            return ticker["last"]
        except Exception as e :
            logger.error(f"Price fetch error : {e}")    
            return None



    # ✅ AUTH TEST (PRIVATE API)
    def get_positions(self):
        return self.exchange.fetch_positions()
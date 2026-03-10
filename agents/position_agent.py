from logs.logger import logger
from config.settings import PRODUCT_SYMBOL

class PositionAgent:

    def __init__(self,client):
        self.client=client

    def has_open_position(self):
        positions=self.client.get_positions()    

        if not positions:
            return False

        for p in positions:
            if p["symbol"] == PRODUCT_SYMBOL and abs(p["size"])>0:
                logger.info("PositionAgent: open position detected") 
                return True  

        return False          


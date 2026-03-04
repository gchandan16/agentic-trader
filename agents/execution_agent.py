from logs.logger import logger
from config.settings import SYMBOL
from config.trade_config import (TRADE_SIZE,STOP_LOSS_PERCENT,TAKE_PROFIT_PERCENT,LIVE_TRADING)

class ExecutionAgent:
    def __init__(self,exchange):
        self.exchange = exchange




    def calculate_position_size(self, price):
        size = TRADE_SIZE / price
        return round(size, 6)  

    def calculate_stop_loss(self, price, side):
        if side == "BUY":
            return price * (1 - STOP_LOSS_PERCENT)

        if side == "SELL":
            return price * (1 + STOP_LOSS_PERCENT)    

    def calculate_take_profit(self, price, side):
        if side == "BUY":
            return price * (1 + TAKE_PROFIT_PERCENT)

        if side == "SELL":
            return price * (1 - TAKE_PROFIT_PERCENT)

    def execute_trade(self, signal, market_state):
        print("executing the trade going on",signal)
        if signal == "HOLD":
            logger.info("ExecutionAgent: No trade signal")
            return

        price = market_state["price"]

        size = self.calculate_position_size(price)
        #MINIMUM Size Check
        if size < 0.00001:
            print("Trade size too small & skipping")
            logger.warning("ExecutionAGnet: Trade skipped due to small size")
            return 

        stop_loss = self.calculate_stop_loss(price, signal)

        take_profit = self.calculate_take_profit(price, signal)

        logger.info(f"Executing {signal}")
        logger.info(f"Size: {size}")
        logger.info(f"Entry Price: {price}")
        logger.info(f"Stop Loss: {stop_loss}")
        logger.info(f"Take Profit: {take_profit}")

        print("Executing Trade")
        print("Side:", signal)
        print("Size:", size)
        print("Entry:", price)
        print("Stop Loss:", stop_loss)
        print("Take Profit:", take_profit)    

        # SAFTY SWITCH
        if not LIVE_TRADING:
            print("Paper Trade Mode - No real order sent")   
            return

        try:
            side=signal.lower()

            order =self.exchange.create_market_order(SYMBOL,side,size)   

            logger.info(f"Order placed :{order}")
            print("Real order executed",order)

        except Exception as e:
            logger.error(f"Execution Error :{str(e)}")
            print("Trade execution failed",e)      
     


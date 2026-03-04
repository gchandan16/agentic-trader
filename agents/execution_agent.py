from logs.logger import logger
from config.settings import SYMBOL
from config.trade_config import (TRADE_SIZE,STOP_LOSS_PERCENT,TAKE_PROFIT_PERCENT)

class ExecutionAgent:
    def __init__(self,exchange):
        self.exchange = exchange


    def execution_trade(self,signal):

        if  signal == "BUY":
            logger.info("ExecutionAgent:BUY order exxecuted ")
            print("Paper Traden -> Buy")

        elif signal == "SELL":
            logger.info("ExecutionAgent:SELL order executed ")      
            print("Paper Trade -> SELL")
        else:
            logger.info("ExecutionAgnet :No Trade executed")
            print("Paper Trade -> No trade Executed")     


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
     


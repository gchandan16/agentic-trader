from logs.logger import logger
from config.settings import PRODUCT_SYMBOL
from config.trade_config import (TRADE_SIZE, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT, LIVE_TRADING)


class ExecutionAgent:
    def __init__(self, client):
        self.client = client

    def calculate_size(self, price):
        """
        Delta India BTCUSD: 1 contract = 1 USD
        So TRADE_SIZE in USD = number of contracts directly
        Minimum order = 1 contract
        """
        contracts = max(1, int(TRADE_SIZE))
        return contracts

    def calculate_stop_loss(self, price, side):
        if side == "buy":
            return round(price * (1 - STOP_LOSS_PERCENT), 2)
        return round(price * (1 + STOP_LOSS_PERCENT), 2)

    def calculate_take_profit(self, price, side):
        if side == "buy":
            return round(price * (1 + TAKE_PROFIT_PERCENT), 2)
        return round(price * (1 - TAKE_PROFIT_PERCENT), 2)

    def execute_trade(self, signal, market_state):

        if signal == "HOLD":
            logger.info("ExecutionAgent: HOLD — no trade")
            print("⏸️  HOLD — skipping trade")
            return

        price = market_state["price"]
        side  = signal.lower()        # "buy" or "sell"
        size  = self.calculate_size(price)
        sl    = self.calculate_stop_loss(price, side)
        tp    = self.calculate_take_profit(price, side)

        print("\n" + "=" * 45)
        print(f"📊 Signal        : {signal}")
        print(f"📦 Product       : {PRODUCT_SYMBOL}")
        print(f"💰 Entry Price   : {price}")
        print(f"📦 Size          : {size} contracts (1 contract = $1)")
        print(f"🛑 Stop Loss     : {sl}")
        print(f"🎯 Take Profit   : {tp}")
        print(f"🔴 Live Trading  : {LIVE_TRADING}")
        print("=" * 45)

        logger.info(f"Trade | {signal} | {PRODUCT_SYMBOL} | Price:{price} | Size:{size} | SL:{sl} | TP:{tp}")

        if not LIVE_TRADING:
            print("📝 PAPER TRADE MODE — no real order sent")
            return

        print(f"🚀 Placing live order on Delta India...")

        order = self.client.place_market_order(PRODUCT_SYMBOL, side, size)

        if order:
            order_id = order.get("id", "unknown")
            logger.info(f"✅ Order success: {order}")
            print(f"✅ Order placed! ID: {order_id}")

            #Place Stop loss order
            sl_order = self.client.place_stop_loss(PRODUCT_SYMBOL,side,size,sl)

            print(f"🛑 Stop Loss order placed at {sl}")

            #Place Take Profit
            tp_order = self.client.place_take_profit(PRODUCT_SYMBOL,side,size,tp)
        else:
            logger.error("Order placement returned None")
            print("❌ Order failed — check logs")

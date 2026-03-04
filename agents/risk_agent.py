from logs.logger import logger
class RiskAgent:
    def __init__(self):
        self.max_risk_per_trade=0.01
        self.daily_loss_limit=0.02
        self.max_trades_per_day=5
        self.trades_taken=0
        self.daily_loss=0

    def approve_trade(self,signal):

        if signal == "HOLD":
            logger.info("RiskAgent:No Trade signal")
            return False
        if self.trades_taken >= self.max_trades_per_day:
            logger.warning("RiskAgent Max trades reached")
            return False
        if self.daily_loss >= self.daily_loss_limit:
            logger.warning("RiskAgent Daily loss limit exceed")
            return False

        logger.info("RiskAgent:Trade Approved")
        self.trades_taken += 1

        return True    


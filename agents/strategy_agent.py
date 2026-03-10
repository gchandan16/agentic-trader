from logs.logger import logger

class StrategyAgent:

    def  __init__(self):
        pass

    def generate_signal(self,market_state):

        if market_state is None:
            return "HOLD"

        trend= market_state["trend"] 
        volatility = market_state["volatility"]       
        volume = market_state["volume_strength"]

        #BUY LOGIC
        if trend=="UP" and volatility=="HIGH" and volume=="STRONG":
            signal="BUY"

        #SELL LOGIC
        elif trend=="DOWN" and volatility=="HIGH" and volume=="STRONG":
            signal="SELL"

        #Otherwise stay safe
        else:
            signal="HOLD"  


        logger.info(f"Strategy Signal :{signal}")    

        return signal  

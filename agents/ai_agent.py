from logs.logger import logger
class AIAgent:
    def __init__(self):
        pass

    def reason(self,market_state,signal):

        if signal == "HOLD":
            decision = {
                "action":"HOLD",
                "confidence":0.0,
                "reason": "Strategy returned HOLD"
            }    
            return decision

        trend= market_agent["trend"]
        volatility =market_state["volatility"]
        volume =market_state["volume_strength"]    
        confidence = 0.5

        if trend == "UP":
            confidence +=0.2

        if volatility == "HIGH":
            confidence +=0.2

        if volume == "STRONG":
            confidence += 0.1

        decision ={
            "action": signal,
            "confidence": round(confidence, 2),
            "reason": "Trend + volatility + volume alignment"
        }       
        logger.info(f"AI Decision: {decision}")

        return decision     
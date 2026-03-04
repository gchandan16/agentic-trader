import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from logs.logger import logger

load_dotenv()

class LLMAgent:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def decide(self, market_state, signal):

        prompt = f"""
You are a professional crypto trader.

Market State:
Price: {market_state['price']}
Trend: {market_state['trend']}
Volatility: {market_state['volatility']}
Volume Strength: {market_state['volume_strength']}

Strategy suggested: {signal}

Respond ONLY in JSON format like this:

{{
 "action": "BUY or SELL or HOLD",
 "confidence": 0.75,
 "reason": "short explanation"
}}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content.strip()

        logger.info(f"LLM Raw Response: {text}")

        try:
            decision = json.loads(text)
        except:
            # fallback if LLM adds extra text
            start = text.find("{")
            end = text.rfind("}") + 1
            decision = json.loads(text[start:end])

        return decision
import time

from agents.market_agent import MarketAgent
from agents.strategy_agent import StrategyAgent
from agents.risk_agent import RiskAgent
from agents.execution_agent import ExecutionAgent
from agents.memory_agent import MemoryAgent
from agents.llm_agent import LLMAgent
from agents.position_agent import PositionAgent
from agents.reflection_agent import ReflectionAgent
from logs.logger import logger

from exchange.delta_client import DeltaClient


class Orchestrator:

    def __init__(self):
        # Single shared client for entire bot
        self.client = DeltaClient()

        # Verify auth on startup
        if not self.client.test_auth():
            raise RuntimeError("❌ Cannot start bot — API auth failed!")

        self.market_agent    = MarketAgent(self.client)
        self.strategy_agent  = StrategyAgent()
        self.llm_agent       = LLMAgent()
        self.risk_agent      = RiskAgent()
        self.position_agent  = PositionAgent(self.client)
        self.execution_agent = ExecutionAgent(self.client)   # pass full client
        self.memory_agent    = MemoryAgent()
        self.reflection_agent = ReflectionAgent()

    def run(self):
        print("\n🤖 Agentic Trader Started!")
        print("=" * 40)

        while True:
            try:
                print("\n----- New Trading Cycle -----")

                # Step 1: Observe market
                market_state = self.market_agent.observe_market()
                if market_state is None:
                    print("⚠️  Market data unavailable — skipping cycle")
                    time.sleep(60)
                    continue

                print(f"k Market: {market_state}")

                # Step 2: Generate signal
                signal = self.strategy_agent.generate_signal(market_state)
                print(f"📡 Strategy Signal: {signal}")

                # Step 3: LLM decision
                decision = self.llm_agent.decide(market_state, signal)
                print(f"🧠 AI Decision: {decision}")

                action=decision["action"]
                confidence=decision["confidence"]

                # Step 4:AI Confidence Filter
                if confidence < 0.7:
                    print("⚠️ Low confidence - skipping trade")
                    continue

                # Step 5: Risk check
                if not self.risk_agent.approve_trade(decision["action"]):
                    print("❌ RiskAgent rejected trade")
                    continue

                # Step 6 
                if self.position_agent.has_open_position():
                    print("Position already open -skipping the trade")    

                
                # Step 7
                self.execution_agent.execute_trade(action,market_state)

                # Step 8 
                self.memory_agent.store_trade(decision,market_state)
                # Step 9
                self.reflection_agent.analyze_trades()
                logger.info("Trading cycle completed")

            except Exception as e:
                print(f"❌ Cycle error: {e}")

            print(f"\n⏳ Sleeping 5 minutes...")
            time.sleep(300)

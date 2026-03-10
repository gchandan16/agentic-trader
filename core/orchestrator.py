import time

from agents.market_agent import MarketAgent
from agents.strategy_agent import StrategyAgent
from agents.risk_agent import RiskAgent
from agents.execution_agent import ExecutionAgent
from agents.memory_agent import MemoryAgent
from agents.llm_agent import LLMAgent

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
        self.execution_agent = ExecutionAgent(self.client)   # pass full client
        self.memory_agent    = MemoryAgent()

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

                # Step 4: Risk check

                approved = self.risk_agent.approve_trade(decision["action"])

                if approved:
                    # Step 5: Execute
                    self.execution_agent.execute_trade(decision["action"], market_state)

                    # Step 6: Remember
                    self.memory_agent.store_trade(decision, market_state)
                else:
                    print("🚫 Trade rejected by RiskAgent")

            except Exception as e:
                print(f"❌ Cycle error: {e}")

            print(f"\n⏳ Sleeping 5 minutes...")
            time.sleep(300)

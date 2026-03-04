import time

from agents.market_agent import MarketAgent
from agents.strategy_agent import StrategyAgent
from agents.ai_agent import AIAgent
from agents.risk_agent import RiskAgent
from agents.execution_agent import ExecutionAgent
from agents.memory_agent import MemoryAgent
from agents.llm_agent import LLMAgent

from exchange.delta_client import DeltaClient


class Orchestrator:

    def __init__(self):

        client = DeltaClient()

        self.market_agent = MarketAgent()
        self.strategy_agent = StrategyAgent()
        self.llm_agent = LLMAgent()
        self.ai_agent = AIAgent()
        self.risk_agent = RiskAgent()
        self.execution_agent = ExecutionAgent(client.exchange)
        self.memory_agent = MemoryAgent()


    def run(self):

        while True:

            print("\n----- New Trading Cycle -----")

            market_state = self.market_agent.observe_market()

            signal = self.strategy_agent.generate_signal(market_state)

            #decision = self.ai_agent.reason(market_state, signal)
            decision = self.llm_agent.decide(market_state,signal)
            print("AI Decision:", decision)

            approved = self.risk_agent.approve_trade(decision["action"])

            if approved:

                self.execution_agent.execute_trade(
                    decision["action"], market_state
                )

                self.memory_agent.store_trade(
                    decision,
                    market_state
                )

            else:

                print("Trade rejected by RiskAgent")

            time.sleep(300)
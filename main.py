from agents.market_agent import MarketAgent
from agents.strategy_agent import StrategyAgent


def main():

    market_agent = MarketAgent()
    strategy_agent = StrategyAgent()

    market_state = market_agent.observe_market()

    print("Market State:", market_state)

    signal = strategy_agent.generate_signal(market_state)

    print("Trading Signal:", signal)


if __name__ == "__main__":
    main()
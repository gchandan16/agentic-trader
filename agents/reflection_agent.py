import json

class ReflectionAgent:

    def analyze_trades(self):
        with open("memory/trade_memory.json","r") as f:
            trades=[json.loads(line) for line in f]

        wins=0
        losses=0

        for t in trades:
            if t.get("pnl",0) >0 :
                wins += 1 
            else:
                losses +=1

        total = wins +losses

        if total == 0:
            return 

        win_rate = wins / total
        print("Win Rate ",win_rate)                    

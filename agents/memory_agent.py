import json
from datetime import datetime

class MemoryAgent:

    def __init__(self):
        self.file = "memory/trade_memory.json"

    def store_trade(self,decision,market_state):
        trade_record={
            "time" :str(datetime.now()),
            "decision":decision,
            "market":market_state
        }    

        try:
            with open(self.file,"a") as f:
                json.dump(trade_record,f)
                f.write("\n")
        except Exception as e:
            print("Memory Agent Error:",e)        
    

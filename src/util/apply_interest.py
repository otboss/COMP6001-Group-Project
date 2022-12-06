from src.Balances import Balances
import time

async def apply_interest(smart_contract: Balances):
    while True:
        time.sleep(smart_contract.getInterestPeriod().seconds)
        smart_contract.addInterest()
from src.Balances import Balances
import time

async def apply_interest(smart_contract: Balances):
    while True:
        time.sleep(smart_contract.getInterestPeriod() * 24 * 60 * 60)
        smart_contract.addInterest()
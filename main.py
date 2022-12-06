from src.Operations import Operations
from src.balances import Balances
from src.liquidity_pool import LiquidityPool
from math import trunc
import sys
import time
import random

def main():
    start_time: int = get_current_time()
    all_params = {
            "--subscriber-count": "the amonut of investors",
            "--execution-duration-in-days": "the literal runtime of the program in days",
            "--rebound-trigger-percentage": "",
            "--interest-rate": "",
            "--interest-period-in-days": "",
            "--buy-sell-ratio": "",
            "--token-y-count": "",
            "--token-x-count": "",
            "--min-buy-amount": "",
            "--max-buy-amount": "",
        } 
    arguments = {}
  
    if sys.argv[-1] == "--help":
            for param in dict.keys(all_params):
                print(param + " -> " + all_params[param] + "\n")
            sys.exit(0)

    if len(sys.argv) < len(dict.keys(all_params)):
        print("missing argument. All parameters are required")
        sys.exit(1)

    for arg in range(len(sys.argv)[1:]):
        if sys.argv[arg] in dict.keys(all_params):
                if sys.argv[arg + 1] == None:
                    print("missing argument for "+sys.argv[arg])
                    sys.exit(1)
                arguments[sys.argv[arg]] = sys.argv[arg + 1]

    smart_contract = Balances(
        sys.argv["--interest-rate"],
        sys.argv["--interest-period-in-days"],
    )

    liquidity_pool = LiquidityPool(
        sys.argv["--token-x-count"],
        sys.argv["--token-y-count"],
        sys.argv["--rebound-trigger-percentage"],
        smart_contract.triggerRebound
    )

    apply_interest(smart_contract)

    # Populate balances
    user_addresses = []
    for i in range(sys.argv["--subscriber-count"]):
        address = random.getrandbits(128)
        smart_contract.setWalletBalance(address, 0)
        user_addresses.append(address)

    while get_current_timestamp() - start_time <= sys.argv["--execution-duration-in-days"] * 24 * 60 * 60 * 1000:
        selected_address = user_addresses[random.randint(0, len(user_addresses)-1)]
        selected_operation: Operations = random.choices(list(Operations), weights=(sys.argv["--buy-sell-ratio"], 1-sys.argv["--buy-sell-ratio"]), k=1)[0]

        if selected_operation == Operations.BUY:
            # TODO: Buy from liquidity pool and update balance for selected address
            pass
        if selected_operation == Operations.SELL:
            # TODO: Sell to liquidity pool and update balance for selected address
            pass

if __name__ == "__main__":
    main()


# Helper Functions

async def apply_interest(smart_contract: Balances):
    while True:
        time.sleep(smart_contract.getInterestPeriod().seconds)
        smart_contract.addInterest()

def get_current_timestamp() -> int:
    return trunc(time()*1000)
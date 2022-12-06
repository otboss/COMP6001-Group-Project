#!/bin/python3

from src.Operations import Operations
from src.Balances import Balances
from src.LiquidityPool import LiquidityPool
from src.Arguments import Arguments
from src.util.get_current_timestamp import get_current_timestamp
from src.util.format_argument import format_argument
from src.util.apply_interest import apply_interest
import sys
import time
import random

def main():
    start_time: int = get_current_timestamp()
    all_params = {
        "--subscriber-count": "the amonut of investors",
        "--execution-duration-in-days": "the literal runtime of the program in days",
        "--rebound-trigger-percentage": "the inflation percent that will trigger an inflationary reset",
        "--interest-rate-percentage": "the percent interest rate wallets will attain",
        "--interest-period-in-days": "the time period in days when all accounts should attain interest",
        "--buy-sell-ratio": "the ratio of buy to sell orders of the simulation",
        "--token-y-count": "the amount of token y to initialize the liquidity pool with",
        "--token-x-count": "the amount of token x to initialize the liquidity pool with",
        "--min-transaction-amount": "the minimum token y a user should buy in the simulation",
        "--max-transaction-amount": "the maximum token y a user should buy in the simulation",
        "--min-transaction-time": "the minimum time in seconds until a new buy or sell is made",
        "--max-transaction-time": "the maximum time in seconds until a new buy or sell is made",
    }

    arguments = Arguments()

    if sys.argv[-1] == "--help":
        print("Required parameters are:\n")
        table_data = []
        max_word_length = 0
        for param in dict.keys(all_params):
            table_data.append([param, all_params[param]])
            if max_word_length < len(param):
                max_word_length = len(param)
        for row in table_data:
            print ("\t" + "".join(word.ljust(max_word_length + 1) for word in row))
        print("\nwhere token x is the input token and token y is the output token for a \033[1mbuy transaction\033[1m\n")
        sys.exit(0)

    if len(sys.argv) < len(dict.keys(all_params)):
        print("missing argument. All parameters are required, use --help for more information")
        sys.exit(1)

    for arg in range(len(sys.argv)[1:]):
        if sys.argv[arg] in dict.keys(all_params):
            if sys.argv[arg + 1] == None:
                print("missing argument for "+sys.argv[arg])
                sys.exit(1)
            value = None
            try:
                expected_type: str = type(arguments[format_argument(sys.argv[arg])]).__name__
                if expected_type == "int":
                    value = int(sys.argv[arg + 1])
                if expected_type == "float":
                    value = float(sys.argv[arg + 1])
                if expected_type == "str":
                    value = str(sys.argv[arg + 1])
                if expected_type == "bool":
                    value = sys.argv[arg + 1].lower() == "true"
            except ValueError:
                print("invalid argument type for "+sys.argv[arg]+". Argument must be of type "+ type(arguments[format_argument(sys.argv[arg])]).__name__)
                sys.exit(1)
            except Exception as e:
                print(e)
                sys.exit(1)
            arguments[format_argument(sys.argv[arg])] = value
        else:
            print("invalid argument passed. Use --help for more information")
            sys.exit(1)

    smart_contract = Balances(
        arguments.interest_rate,
        arguments.interest_period_in_days,
    )

    liquidity_pool = LiquidityPool(
        arguments.token_x_count,
        arguments.token_y_count,
        arguments.rebound_trigger_percentage,
        smart_contract.triggerRebound,
    )

    apply_interest(smart_contract)

    # Populate balances
    user_addresses = []
    for i in range(arguments.subscriber_count):
        address = random.getrandbits(128)
        smart_contract.setWalletBalance(address, 0)
        user_addresses.append(address)

    # Start simulation
    while get_current_timestamp() - start_time <= arguments.execution_duration_in_days * 24 * 60 * 60 * 1000:
        time.sleep(random.randint(arguments.min_transaction_time, arguments.max_transaction_time))
        selected_address = user_addresses[random.randint(0, len(user_addresses)-1)]
        selected_operation: Operations = random.choices(list(Operations), weights=(arguments.buy_sell_ratio, 1-arguments.buy_sell_ratio), k=1)[0]
        wallet_balance = smart_contract.getWalletBalance(selected_address)

        if wallet_balance == 0 or selected_operation == Operations.BUY:
            bought_tokens = liquidity_pool.buyY(
                random.randint(
                    arguments.min_transaction_amount,
                    arguments.max_transaction_amount,
                )
            )
            smart_contract.setWalletBalance(selected_address, bought_tokens)

        if selected_operation == Operations.SELL:
            sold_tokens = random.uniform(
                wallet_balance * 0.25,
                wallet_balance,
            )
            liquidity_pool.sellY(sold_tokens)
            smart_contract.setWalletBalance(selected_address, sold_tokens)

    # TODO: print findings
    sys.exit(0)

if __name__ == "__main__":
    main()
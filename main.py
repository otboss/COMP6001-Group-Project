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
import os
from datetime import datetime

def main():
    start_time: int = get_current_timestamp()
    all_params = {
        "--subscriber-count": "the amonut of investors",
        "--execution-duration-in-days": "the literal runtime of the program in days",
        "--rebound-trigger-percentage": "the inflation percent that will trigger an inflationary reset",
        "--interest-rate-percentage": "the percent interest rate wallets will attain",
        "--interest-period-in-days": "the time period in days when all accounts should attain interest",
        "--buy-sell-ratio": "the ratio of buy to sell orders of the simulation (a number from 0-1)",
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

    param = sys.argv[1:]
    for arg in range(0, len(param), 2):
        if param[arg] in dict.keys(all_params):
            if param[arg + 1] == None:
                print("missing argument for "+param[arg])
                sys.exit(1)
            value = None
            try:
                expected_type: str = type(getattr(arguments, format_argument(param[arg]))).__name__
                if expected_type == "int":
                    value = int(param[arg + 1])
                if expected_type == "float":
                    value = float(param[arg + 1])
                if expected_type == "str":
                    value = str(param[arg + 1])
                if expected_type == "bool":
                    value = param[arg + 1].lower() == "true"
            except ValueError:
                print("invalid argument type for "+param[arg]+". Argument must be of type "+ type(getattr(arguments, format_argument(param[arg]))).__name__)
                sys.exit(1)
            except Exception as e:
                print(e)
                sys.exit(1)
            setattr(arguments, format_argument(param[arg]), value)
        else:
            print("invalid argument passed. Use --help for more information")
            sys.exit(1)

    smart_contract = Balances(
        arguments.interest_rate_percentage,
        arguments.interest_period_in_days
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

    output_path = "./output"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    folder_path = "%s/%s"%(output_path, str(datetime.now()))
    os.makedirs(folder_path)

    price_log_path = "%s/%s"%(folder_path, "prices.csv")
    price_log_file = open(price_log_path, "a")
    price_log_file.write("price_y,total_x_supply,total_y_supply,timestamp\n")
    price_log_file.close()

    transaction_log_path = "%s/%s"%(folder_path, "transactions.csv")
    transaction_log_file = open(transaction_log_path, "a")
    transaction_log_file.write("transaction,buyer,quantity,wallet_balance,timestamp\n")
    transaction_log_file.close()

    # Start simulation
    while get_current_timestamp() - start_time <= arguments.execution_duration_in_days * 24 * 60 * 60 * 1000:
        time.sleep(random.uniform(arguments.min_transaction_time, arguments.max_transaction_time))
        selected_address = user_addresses[random.randint(0, len(user_addresses)-1)]
        selected_operation: Operations = random.choices(list(Operations), weights=(arguments.buy_sell_ratio, 1-arguments.buy_sell_ratio), k=1)[0]
        wallet_balance = smart_contract.getWalletBalance(selected_address)
        quantity = 0

        if wallet_balance == 0 or selected_operation == Operations.BUY:
            selected_operation = Operations.BUY
            quantity = liquidity_pool.buyY(
                random.randint(
                    arguments.min_transaction_amount,
                    arguments.max_transaction_amount,
                )
            )
            wallet_balance += quantity
            smart_contract.setWalletBalance(selected_address, wallet_balance)

        if selected_operation == Operations.SELL:
            quantity = random.uniform(
                wallet_balance * 0.25,
                wallet_balance,
            )
            liquidity_pool.sellY(quantity)
            wallet_balance -= quantity
            smart_contract.setWalletBalance(selected_address, wallet_balance)

        price_log_file = open(price_log_path, "a")
        price_log_file.write("%f,%f,%f,%s\n"%(liquidity_pool.getPriceY(), liquidity_pool.getX(), liquidity_pool.getY(), str(datetime.now())))
        price_log_file.close()

        transaction_log_file = open(transaction_log_path, "a")
        transaction_log_file.write("%s,%s,%f,%s,%s\n"%(selected_operation.name, selected_address, quantity, wallet_balance, str(datetime.now())))
        transaction_log_file.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
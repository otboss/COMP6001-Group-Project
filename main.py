#!/bin/python3

from src.Operations import Operations
from src.Balances import Balances
from src.LiquidityPool import LiquidityPool
from src.Arguments import Arguments
from src.util.format_argument import format_argument
from src.exceptions.insufficient_funds_exception import InsufficientFundsException
from datetime import datetime
from math import floor
import sys
import random
import os

def main():
    all_params = {
        "--subscriber-count": "the amonut of investors",
        "--subscriber-growth-percentage": "a percent value (0-100) representing the user growth per day",
        "--execution-duration-in-days": "the literal runtime of the program in days",
        "--stagnation-day": "a number from 0-1 representing the fractional day when no new buys are made",
        "--min-transactions-per-day": "the minimum number of transactions to simulate per day",
        "--max-transactions-per-day": "the maximum number of transactions to simulate per day",
        "--rebound-trigger-percentage": "the inflation percent that will trigger an inflationary reset",
        "--interest-rate-percentage": "the percent interest rate wallets will attain",
        "--interest-period-in-days": "the time period in days when all accounts should attain interest",
        "--buy-sell-ratio": "the ratio of buy to sell orders of the simulation (a number from 0-1)",
        "--token-y-count": "the amount of token y to initialize the liquidity pool with",
        "--token-x-count": "the amount of token x to initialize the liquidity pool with",
        "--min-transaction-amount": "the minimum token y a user should buy in the simulation",
        "--max-transaction-amount": "the maximum token y a user should buy in the simulation",
        "--test-wallet": "a custom wallet to run through the simulation",
        "--test-wallet-balance": "the balance to initialize the test wallet with",
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
            print("invalid argument "+arg+" passed. Use --help for more information")
            sys.exit(1)

    smart_contract = Balances(
        arguments.interest_rate_percentage,
        arguments.interest_period_in_days
    )

    liquidity_pool = LiquidityPool(
        arguments.token_x_count,
        arguments.token_y_count,
    )

    # Populate balances
    user_addresses = []
    for _ in range(arguments.subscriber_count):
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
    price_log_file.write("price_y,total_x_supply,total_y_supply,day,transaction_no\n")
    price_log_file.close()

    transaction_log_path = "%s/%s"%(folder_path, "transactions.csv")
    transaction_log_file = open(transaction_log_path, "a")
    transaction_log_file.write("transaction,buyer,quantity,wallet_balance,day,transaction_no\n")
    transaction_log_file.close()

    test_wallet_value_log_path = "%s/%s"%(folder_path, "test-wallet-value.csv")
    test_wallet_value_file = open(test_wallet_value_log_path, "a")
    test_wallet_value_file.write("value,day\n")
    test_wallet_value_file.close()

    for day_count in range(arguments.execution_duration_in_days):
        smart_contract.addInterest()
        liquidity_pool.resetTotalDailyWithdrawl()

        # Transactions per day
        for transaction_count in range(random.randint(arguments.min_transactions_per_day, arguments.max_transactions_per_day)):
            selected_address = user_addresses[random.randint(0, len(user_addresses)-1)]
            selected_operation: Operations = random.choices(list(Operations), weights=(arguments.buy_sell_ratio, 1-arguments.buy_sell_ratio), k=1)[0]
            wallet_balance = smart_contract.getWalletBalance(selected_address)
            quantity = 0

            if day_count >= round(arguments.stagnation_day * arguments.execution_duration_in_days):
                selected_operation = selected_operation = Operations.SELL

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

                if liquidity_pool.getPriceY() > liquidity_pool.getAllTimeHighY():
                    liquidity_pool.setAllTimeHighY(liquidity_pool.getPriceY())  
                    liquidity_pool.setAllTimeHighXTokenCount(liquidity_pool.getX()) 
                    liquidity_pool.setAllTimeHighYTokenCount(liquidity_pool.getY())

            try:
                if selected_operation == Operations.SELL:
                    user_holding = (wallet_balance / liquidity_pool.getY() * 100)
                
                    dtp_ratio: float = user_holding < 1 and 1 or \
                        1 <= user_holding <= 10 and liquidity_pool.getDailyTakeProfitCoefficient() / user_holding or 0.1

                    total_withdrawl = liquidity_pool.getTotalDailyWithdrawl(selected_address)
                    origin_wallet_balance = total_withdrawl + wallet_balance

                    daily_limit = origin_wallet_balance * (dtp_ratio / 100)

                    quantity = random.uniform(
                        0,
                        daily_limit,
                    )

                    able_to_sell = quantity > 0 and total_withdrawl + quantity <= daily_limit
                    if able_to_sell:
                        liquidity_pool.sellY(quantity)
                        liquidity_pool.setTotalDailyWithdrawl(selected_address, total_withdrawl + quantity)
                        wallet_balance -= quantity
                        smart_contract.setWalletBalance(selected_address, wallet_balance)

                    if liquidity_pool.calculateInflationPercent() >= arguments.rebound_trigger_percentage:
                        rebound_amount = \
                            liquidity_pool.getAllTimeHighXTokenCount() / (liquidity_pool.getAllTimeHighYTokenCount() / liquidity_pool.getAllTimeHighXTokenCount()) - \
                                liquidity_pool.getX() / (liquidity_pool.getY() / liquidity_pool.getX())
                        smart_contract.triggerRebound(rebound_amount)

                    if not able_to_sell:
                        continue 

            except InsufficientFundsException as e:
                print(e)
                continue

            price_log_file = open(price_log_path, "a")
            price_log_file.write("%f,%f,%f,%d,%d\n"%(liquidity_pool.getPriceY(), liquidity_pool.getX(), liquidity_pool.getY(), day_count + 1, transaction_count))
            price_log_file.close()

            transaction_log_file = open(transaction_log_path, "a")
            transaction_log_file.write("%s,%s,%f,%s,%d,%d\n"%(selected_operation.name, selected_address, quantity, wallet_balance, day_count + 1, transaction_count))
            transaction_log_file.close()

            test_wallet_value_file = open(test_wallet_value_log_path, "a")
            test_wallet_value_file.write("%f,%s\n"%(arguments.test_wallet_balance * liquidity_pool.getPriceY(), day_count + 1))
            test_wallet_value_file.close()

        # User growth
        current_user_addresses = user_addresses
        for _ in range(floor(len(current_user_addresses) * arguments.subscriber_growth_percentage / 100)):
            address = random.getrandbits(128)
            smart_contract.setWalletBalance(address, 0)
            user_addresses.append(address)
    sys.exit(0)

if __name__ == "__main__":
    main()
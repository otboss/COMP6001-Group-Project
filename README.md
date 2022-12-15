# Uniqo-Token-Market-Simulator

### Description
This project serves as simulator for the Uniqo token in order to study its long term behaviour

### Documentation
Documentation for the Uniqo token can be found at
<a href="https://docs.uniqo.finance">https://docs.uniqo.finance</a>


### Parameters
```
Required parameters are:

        --subscriber-count             the amonut of investors        
        --subscriber-growth-percentage a percent value (0-100) representing the user growth per day
        --execution-duration-in-days   the literal runtime of the program in days
        --stagnation-day               a number from 0-1 representing the fractional day when no new buys are made
        --min-transactions-per-day     the minimum number of transactions to simulate per day
        --max-transactions-per-day     the maximum number of transactions to simulate per day
        --rebound-trigger-percentage   the inflation percent that will trigger an inflationary reset
        --interest-rate-percentage     the percent interest rate wallets will attain
        --interest-period-in-days      the time period in days when all accounts should attain interest
        --buy-sell-ratio               the ratio of buy to sell orders of the simulation (a number from 0-1)
        --token-y-count                the amount of token y to initialize the liquidity pool with
        --token-x-count                the amount of token x to initialize the liquidity pool with
        --min-transaction-amount       the minimum token y a user should buy in the simulation
        --max-transaction-amount       the maximum token y a user should buy in the simulation
        --test-wallet                  a custom wallet to run through the simulation
        --test-wallet-balance          the balance to initialize the test wallet with

where token x is the input token and token y is the output token for a buy transaction
```
This information can be viewed anytime by running the command:
```
python3 main.py --help
```


### Sample Command:
```
python3 main.py \
--subscriber-count 125 \
--subscriber-growth-percentage 0.0304 \
--execution-duration-in-days 365 \
--stagnation-day 0.1 \
--min-transactions-per-day 3000 \
--max-transactions-per-day 4000 \
--rebound-trigger-percentage 7.0 \
--interest-rate-percentage 1.0 \
--interest-period-in-days 1 \
--buy-sell-ratio 0.1 \
--token-y-count 1000000000 \
--token-x-count 1000000 \
--min-transaction-amount 1000 \
--max-transaction-amount 10000 \
--test-wallet 262738840847910164415648694271131068748 \
--test-wallet-balance 1000
```
The command above simulated worst case market conditions, where roughly 90% of all transacton will be sell transactions (buy-sell-ratio = 0.1) with a stagnation day set at 10% of the total days (stagnation-day = 0.1), meaning all following transaction will be sell orders.

Once complete CSV files will be generated to the 'output' directory

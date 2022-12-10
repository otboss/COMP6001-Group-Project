# Uniqo-Token-Market-Simulator

### Description
This project serves as simulator for the Uniqo token in order to study its long term behaviour

### Documentation
Documentation can be found at
<a href="https://docs.uniqo.finance">https://docs.uniqo.finance</a>

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
--min-transaction-time 0.2 \
--max-transaction-time 1.0 \
--test-wallet 262738840847910164415648694271131068748 \
--test-wallet-balance 1000
```

Once complete CSV files will be generated in an 'output' directory

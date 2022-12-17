from datetime import timedelta

class Balances:
    __balances: dict[str, float] = {}
    __interest_rate: float = 0.0

    def __init__(self, interestRate: float) -> None:
        self.__interest_rate = interestRate

    def addInterest(self) -> None:
        for walletAddress in self.__balances:
            self.__balances[walletAddress] += self.__balances[walletAddress] * self.__interest_rate / 100
    
    def setWalletBalance(self, wallet_address: str, balance: float) -> None:
        self.__balances[wallet_address] = balance

    def getWalletBalance(self, walletAddress: str) -> float:
        return self.__balances[walletAddress]

    def triggerRebound(self, val) -> None:
        share = val / len(dict.keys(self.__balances))
        for balance in self.__balances:
            if self.__balances[balance] - share < 0:
                self.__balances[balance] = 0
                continue
            self.__balances[balance] -= share

    def getInterestRate(self) -> float:
        return self.__interest_rate

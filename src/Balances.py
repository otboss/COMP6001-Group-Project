from datetime import timedelta

class Balances:
    __balances: dict[str, float] = {}
    __interest_rate: float = 0
    __interest_period: timedelta = timedelta(days=365.25)

    def __init__(self, interestRate: float, interestPeriod: timedelta) -> None:
        self.__interest_rate = interestRate
        self.__interest_period = interestPeriod

    def addInterest(self) -> None:
        for walletAddress in self.__balances:
            self.__balances[walletAddress] += self.__balances[walletAddress] * self.__interest_rate / 100
    
    def setWalletBalance(self, walletAddress: str, balance: float) -> None:
        self.__balances[walletAddress] = balance

    def getWalletBalance(self, walletAddress: str) -> float:
        return self.__balances[walletAddress]

    def triggerRebound(self, val) -> None:
        share = val / len(dict.keys(self.__balances))
        for balance in self.__balances:
            self.__balances[balance] -= share

    def getInterestRate(self) -> float:
        return self.__interest_rate

    def getInterestPeriod(self) -> timedelta:
        return self.__interest_period

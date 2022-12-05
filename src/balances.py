from datetime import timedelta

class Balances:
    __balances: dict[str, float] = {}
    __interestRate: float = 0
    __interestPeriod: timedelta = timedelta(days=365.25)

    def __init__(self, interestRate: float, interestPeriod: timedelta) -> None:
        self.__interestRate = interestRate
        self.__interestPeriod = interestPeriod

    def addInterest(self) -> None:
        for walletAddress in self.__balances:
            self.__balances[walletAddress] += self.__balances[walletAddress] * self.__interestRate / 100
    
    def setWalletBalance(self, walletAddress: str, balance: float) -> None:
        self.__balances[walletAddress] = balance

    def getWalletBalance(self, walletAddress: str) -> float:
        return self.__balances[walletAddress]

    def triggerRebound(self) -> None:
        # TODO:
        pass

    def getInterestRate(self) -> float:
        return self.__interestRate

    def getInterestPeriod(self) -> timedelta:
        return self.__interestPeriod

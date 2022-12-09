from time import time
from math import trunc
from src.exceptions.insufficient_funds_exception import InsufficientFundsException

class LiquidityPool:
    __x: float = 0
    __y: float = 0
    __initial_x: float = 0
    __initial_y: float = 0
    __creation_timestamp: int = trunc(time()*1000)
    __daily_take_profit_coefficient: float = 0.3
    __total_daily_withdrawl: dict[str, float] = {}

    def __init__(self, x: float, y: float) -> None:
        self.__x = x
        self.__y = y
        self.__initial_x = x
        self.__initial_y = y

    def getK(self) -> float:
        return self.__initial_x * self.__initial_y

    def sellY(self, y: float) -> float:
        deltaX = self.__x - (self.getK()/(self.__y + y))
        if self.__x < deltaX:
            raise InsufficientFundsException("not enough x tokens left in pool to disburse")
        self.__x -= deltaX
        self.__y += y
        return deltaX

    def buyY(self, x: float) -> float:
        deltaY = self.__y - (self.getK() / (self.__x + x))
        if self.__y < deltaY:
            raise InsufficientFundsException("not enough y tokens left in pool to disburse")        
        self.__x += x
        self.__y -= deltaY
        return deltaY

    def calculateInflationPercent(self):
        return 100 - (self.__x / self.__y) / (self.__initial_x / self.__initial_y) * 100

    def calculateDailyTakeProfit(self, wallet_balance: float) -> float:
        return self.__daily_take_profit_coefficient /  (wallet_balance / self.__y * 100)

    def getPriceX(self) -> float:
        return self.__y/self.__x

    def getPriceY(self) -> float:
        return self.__x/self.__y
    
    def getCreationTimestamp(self) -> int:
        return self.__creation_timestamp

    def getX(self) -> float:
        return self.__x

    def getY(self) -> float:
        return self.__y

    def getDailyTakeProfitCoefficient(self) -> float:
        return self.__daily_take_profit_coefficient

    def getTotalDailyWithdrawl(self, wallet_address: str) -> float:
        try:
            return self.__total_daily_withdrawl[wallet_address]
        except KeyError:
            return 0

    def setTotalDailyWithdrawl(self, wallet_address: str, withdrawl_amount: float) -> None:
        self.__total_daily_withdrawl[wallet_address] = withdrawl_amount

    def resetTotalDailyWithdrawl(self) -> None:
        self.__total_daily_withdrawl = {}
            
from time import time
from math import trunc

class LiquidityPool:
    __x: float = 0
    __y: float = 0
    __initialX: float = 0
    __initialY: float = 0
    __creationTimestamp: int = trunc(time()*1000)
    __reboundTriggerPercentage: float = 0
    __reboundTriggerCallback: None

    def __init__(self, x: float, y: float, reboundTriggerPercentage: float, reboundTriggerCallback:None) -> None:
        self.__x = x
        self.__y = y
        self.__initialX = x
        self.__initialY = y
        self.__reboundTriggerPercentage = reboundTriggerPercentage
        self.__reboundTriggerCallback = reboundTriggerCallback

    def getK(self) -> float:
        return self.__initialX * self.__initialY

    def sellY(self, y: float) -> float:
        deltaX = self.getK() / (self.__y - y) - self.__x
        self.__x -= deltaX
        self.__y += y
        if ((self.__y / self.__x) / (self.__initialY / self.__initialX)) * 100 >= self.__reboundTriggerPercentage:
            rebound_amount = 0
            # TODO: Get function to calculate the total amount to be burned as part of rebound
            # rebound_amount = (y / self.__x) / (self.__initialY / self.__initialX) = 1
            self.__reboundTriggerCallback(rebound_amount)

        return deltaX

    def buyY(self, x: float) -> float:
        deltaY = self.__y - self.getK() / (self.__x + x)
        self.__x += x
        self.__y -= deltaY
        return deltaY

    def getPriceX(self) -> float:
        return self.__x/self.__y

    def getPriceY(self) -> float:
        return self.__y/self.__x
    
    def getCreationTimestamp(self) -> int:
        return self.__creationTimestamp
from time import time
from math import trunc

class LiquidityPool:
    __x: float = 0
    __y: float = 0
    __initialX: float = 0
    __initialY: float = 0
    __creationTimestamp: int = trunc(time()*1000)
    __reboundTriggerPercentage: float = 0
    __reboundTriggerCallback: function

    def __init__(self, x: float, y: float, reboundTriggerPercentage: float, reboundTriggerCallback:function) -> None:
        self.__x = x
        self.__y = y
        self.__initialX = x
        self.__initialY = y
        self.__reboundTriggerPercentage = reboundTriggerPercentage
        self.__reboundTriggerCallback = reboundTriggerCallback

    def getK(self) -> float:
        return self.__initialX * self.__initialY

    def buyX(self, y: float) -> float:
        deltaX = self.getK() / (self.__y - y) - self.__x
        self.__x -= deltaX
        self.__y += y

        if ((self.__y / self.__x) / (self.__initialY / self.__initialX)) * 100 >= self.__reboundTriggerPercentage:
            self.__reboundTriggerCallback()

        return deltaX

    def buyY(self, x: float) -> float:
        deltaY = self.__y - self.getK() / (self.__x + x)
        self.__x += x
        self.__y -= deltaY
        return deltaY

    def getPriceX(self) -> float:
        return self.__y/self.__x

    def getPriceY(self) -> float:
        return self.__y/self.__x
    
    def getCreationTimestamp(self) -> int:
        return self.__creationTimestamp
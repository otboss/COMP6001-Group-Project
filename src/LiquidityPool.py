from time import time
from math import trunc

class LiquidityPool:
    __x: float = 0
    __y: float = 0
    __initial_x: float = 0
    __initial_y: float = 0
    __creation_timestamp: int = trunc(time()*1000)
    __rebound_trigger_percentage: float = 0
    __rebound_trigger_callback: None

    def __init__(self, x: float, y: float, reboundTriggerPercentage: float, reboundTriggerCallback:None) -> None:
        self.__x = x
        self.__y = y
        self.__initial_x = x
        self.__initial_y = y
        self.__rebound_trigger_percentage = reboundTriggerPercentage
        self.__rebound_trigger_callback = reboundTriggerCallback

    def getK(self) -> float:
        return self.__initial_x * self.__initial_y

    def sellY(self, y: float) -> float:
        deltaX = self.getK() / (self.__y - y) - self.__x
        self.__x -= deltaX
        self.__y += y

        # TODO: Review rebound implementation
        rebound_trigger_quantity = (self.__initial_y / self.__initial_x) * self.__rebound_trigger_percentage/100
        if ((self.__y / self.__x) / (self.__initial_y / self.__initial_x)) >= rebound_trigger_quantity:
            rebound_amount = (self.__x * self.__initial_y) / self.__initial_x
            self.__rebound_trigger_callback(rebound_amount)

        return deltaX

    def buyY(self, x: float) -> float:
        deltaY = self.__y - self.getK() / (self.__x + x)
        self.__x += x
        self.__y -= deltaY
        return deltaY

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
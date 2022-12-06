from math import trunc
from time import time

def get_current_timestamp() -> int:
    return trunc(time()*1000)
import math
import random


def generate_custom_exponential(scale=None, upper_limit=None):
    while True:
        u = random.random()
        num = -math.log(1-u) / (1/scale)
        num = round(num)
        if 1 <= num <= upper_limit:
            return num

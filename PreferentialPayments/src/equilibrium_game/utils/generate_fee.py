import math
import random
import numpy as np


def generate_custom_exponential(scale=1.0, upper_limit=250):
    while True:
        u = random.random()
        num = -math.log(1 - u) / (1 / scale)
        num = round(num)
        if 1 <= num <= upper_limit:
            return num

def generate_fee_uniform(min_fee, max_fee):
    return int(np.random.uniform(min_fee, max_fee))

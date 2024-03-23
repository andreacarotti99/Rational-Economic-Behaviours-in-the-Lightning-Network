import math

import numpy as np


def f(c: float, dist_func: str):
    """
     the total demand entering/leaving node v might be proportional to f(capacity(v)),
     for some function f. For example, f(c) = sort(c).
     In this case f(x) = x
    """
    if dist_func == "linear":
        return c
    elif dist_func == "quadratic":
        return float(c**2)
    elif dist_func == "cubic":
        return float(c**3)
    elif dist_func == "exponential":
        return math.exp(c)
    return





import numpy as np


def min_max_normalize(x, x_min=0, x_max=1):
    """
    Perform min-max normalization on the input data to scale it to the specified range.
    """
    return (x - x_min) / (x_max - x_min)

def z_score_normalize(x, mean, std_dev):
    return (x - mean) / std_dev

import math
import random
import numpy as np
from matplotlib import pyplot as plt


def generate_exponential_number_numpy(scale=1.0, upper_limit=250):
    while True:
        num = np.random.exponential(scale)
        num = round(num)
        if 1 <= num <= upper_limit:
            return num

# Test the function

def generate_custom_exponential(scale=1.0, upper_limit=250):
    while True:
        u = random.random()
        num = -math.log(1 - u) / (1 / scale)
        num = round(num)
        if 1 <= num <= upper_limit:
            return num

# Test the function
numpy_data = [generate_exponential_number_numpy(scale=25) for _ in range(1000)]
math_data = [generate_custom_exponential(scale=25) for _ in range(1000)]

# Plotting
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(numpy_data, bins=range(1, 251), color='blue', alpha=0.7)
plt.title('Numpy Exponential Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.subplot(1, 2, 2)
plt.hist(math_data, bins=range(1, 251), color='green', alpha=0.7)
plt.title('Custom Exponential Distribution')
plt.xlabel('Value')
plt.tight_layout()
plt.show()

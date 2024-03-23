import random
from src.utils.normalize import z_score_normalize, min_max_normalize
import math

def weight_function_inverse_log_cap(u, v, edge_data):
    channels = list(edge_data.keys())
    max_cap_channel = channels[0]
    max_cap = edge_data[max_cap_channel]['capacity']
    if len(channels) > 1:
        for channel in channels:
            cap = edge_data[channel]['capacity']
            if cap > max_cap:
                max_cap = cap
                max_cap_channel = channel
    else:
        max_cap_channel = channels[0]
    return - math.log(1 / max_cap)

def weight_function_fee(u,v, edge_data):
    channels = list(edge_data.keys())
    min_fee_channel = channels[0]  # Initialize with the first channel
    min_fee = edge_data[min_fee_channel]['fee']
    if len(channels) > 1:
        for channel in channels:
            fee = edge_data[channel]['fee']
            if fee < min_fee:
                min_fee = fee
                min_fee_channel = channel
    else:
        min_fee_channel = channels[0]
    return edge_data[min_fee_channel]['fee']

def weight_function_min_max(u, v, edge_data):
    channels = list(edge_data.keys())

    min_fee_channel = channels[0]  # Initialize with the first channel
    min_fee = edge_data[min_fee_channel]['fee']
    min_cap = edge_data[min_fee_channel]['capacity']
    alfa = edge_data[min_fee_channel]['alfa']
    fee_min_max = min_max_normalize(min_fee, 0, edge_data[min_fee_channel]['max_fee'])
    cap_min_max = min_max_normalize(min_cap, 0, edge_data[min_fee_channel]['max_cap'])
    # print(min_cap)
    min_fun = fee_min_max + alfa * (1 / cap_min_max)

    if len(channels) > 1:
        for channel in channels[1:]:
            fee = edge_data[channel]['fee']
            # alfa = edge_data[channel]['alfa']
            fee_min_max = min_max_normalize(fee, 0, edge_data[channel]['max_fee'])
            capacity = int(edge_data[channel]['capacity'])
            # print(capacity)
            cap_min_max = min_max_normalize(capacity, 0, edge_data[channel]['max_cap'])
            fun = fee_min_max + alfa * (1 / cap_min_max)
            if fun < min_fun:
                min_fun = fun
                # min_fun_channel = channel
    # print(f"w = {fee_min_max} + {alfa} * (1 / {cap_min_max}) = {min_fun}")
    return min_fun


def weight_function_min_max_second_version(u, v, edge_data):
    # Find the channel with the minimum fee using min() with a key argument
    min_fee_channel = min(edge_data, key=lambda ch: edge_data[ch]['fee'])

    # Extract data only once to avoid repeated dictionary lookups
    channel_data = edge_data[min_fee_channel]
    fee = channel_data['fee']
    alfa = channel_data['alfa']
    max_fee = channel_data['max_fee']
    capacity = int(channel_data['capacity'])
    max_cap = channel_data['max_cap']

    # Check for zero capacity to avoid division by zero
    if capacity == 0:
        raise ValueError(f"Capacity is zero for channel {channel_data['channel']}")

    # Assuming min_max_normalize is a separate function that's already optimized
    fee_min_max = min_max_normalize(fee, 0, max_fee)
    capacity_min_max = min_max_normalize(capacity, 0, max_cap)

    # Calculate the weighted function
    fun = fee_min_max + alfa * (1 / capacity_min_max)

    return fun


def weight_function_z_score(u, v, edge_data):
    channels = list(edge_data.keys())
    min_fee_channel = channels[0]  # Initialize with the first channel
    min_fee = edge_data[min_fee_channel]['fee']

    if len(channels) > 1:
        for channel in channels:
            fee = edge_data[channel]['fee']
            if fee < min_fee:
                min_fee = fee
                min_fee_channel = channel
    else:
        min_fee_channel = channels[0]

    print(channels)
    alfa = edge_data[min_fee_channel]['alfa']

    fee = edge_data[min_fee_channel]['fee']
    fee_z_score = z_score_normalize(fee, edge_data[min_fee_channel]['mean_fee'], edge_data[min_fee_channel]['std_dev_fee'])
    fee_min_max = min_max_normalize(fee, 0, edge_data[min_fee_channel]['max_fee'])

    capacity = int(edge_data[min_fee_channel]['capacity'])
    capacity_z_score = z_score_normalize(capacity, edge_data[min_fee_channel]['mean_cap'], edge_data[min_fee_channel]['std_dev_cap'])
    capacity_min_max = min_max_normalize(capacity, 0, edge_data[min_fee_channel]['max_cap'])

    print(f'fee: {fee}')

    print(f"mean fee: {edge_data[min_fee_channel]['mean_fee']}")
    print(f"std dev fee: {edge_data[min_fee_channel]['std_dev_fee']}")

    print(f'fee min max: {fee_min_max}')
    print(f'cap min max: {capacity_min_max}')


    print(f'fee z score: {fee_z_score}')
    print(f'cap z score: {capacity_z_score}')
    fun = fee_z_score + alfa * (1 / capacity_z_score)
    # print(f'from {u} to {v} weight: {fun}')
    return fun

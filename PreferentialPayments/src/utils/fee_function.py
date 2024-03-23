import random

from src.utils.normalize import min_max_normalize


def fee_function(u, v, edge_data):
   channels = list(edge_data.keys())

   min_fee_channel = channels[0]  # Initialize with the first channel
   min_fee = edge_data[min_fee_channel]['fee']
   min_cap = edge_data[min_fee_channel]['capacity']
   alfa = edge_data[min_fee_channel]['alfa']
   fee_min_max = min_max_normalize(min_fee, 0, edge_data[min_fee_channel]['max_fee'])
   cap_min_max = min_max_normalize(min_cap, 0, edge_data[min_fee_channel]['max_cap'])

   min_fun = fee_min_max + alfa * (1 / cap_min_max)
   min_fun_channel = channels[0]

   if len(channels) > 1:
       for channel in channels[1:]:
           fee = edge_data[channel]['fee']
           # alfa = edge_data[channel]['alfa']
           fee_min_max = min_max_normalize(fee, 0, edge_data[channel]['max_fee'])
           capacity = int(edge_data[channel]['capacity'])
           cap_min_max = min_max_normalize(capacity, 0, edge_data[channel]['max_cap'])
           fun = fee_min_max + alfa * (1 / cap_min_max)
           if fun < min_fun:
               min_fun = fun
               min_fun_channel = channel
   return edge_data[min_fun_channel]['fee']

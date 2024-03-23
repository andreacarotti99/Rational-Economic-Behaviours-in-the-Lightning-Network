import math
import random

import numpy as np
from src.Channel import Channel
from src.ChannelGraph import ChannelGraph
from src.equilibrium_game.utils.generate_fee import generate_custom_exponential


def edit_randomly_all_channels(G: ChannelGraph, target_node: str, max_fee=250) -> [Channel]:
    edited_channels = []

    for dest_node in G.get_connected_nodes(target_node):

        for ch in G.get_channels(target_node, dest_node):

            new_fee_value = generate_custom_exponential(scale=50, upper_limit=max_fee)

            # print(f'trying replacing {ch.base_fee} + {ch.ppm * 10} value: ', new_fee_value)

            if G.edit_channel(target_node, dest_node, ch.short_channel_id, 'fee', new_fee_value):
                edited_channels.append(ch)
            else:
                print(f'channel {ch.short_channel_id} not edited...')
                return []
    # print(edited_channels)
    return edited_channels

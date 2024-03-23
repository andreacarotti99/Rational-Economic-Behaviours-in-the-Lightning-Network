import logging
import random

from src import Channel, ChannelGraph
from src.equilibrium_game.utils.ridistribute_capacity_of_closed_channels import ridistribute_capacity_of_closed_channel


def close_all_channels(G: ChannelGraph, target_node: str) -> [Channel]:
    closed_channels = []
    # print(f"Node {target_node[0:5]} picked, closing all its channels...")
    for dest_node in G.get_connected_nodes(target_node):
        for ch in G.get_channels(target_node, dest_node):
            # print(ch)
            if G.close_channel_bilateral(target_node, dest_node, ch.short_channel_id):
                # logging.debug('closed ch with %s capacity: %d ch_id: %s', dest_node, ch.capacity, ch.short_channel_id)
                # print(f'|__CLOSED ch with {dest_node[0:5]}, capacity: {ch.capacity} ch_id: {ch.short_channel_id}')
                closed_channels.append(ch)
                ridistribute_capacity_of_closed_channel(G, dest_node, ch)
            else:
                print(f'channel {ch.short_channel_id} not closed...')
                return []

    return closed_channels




def close_randomly_n_channels(G: ChannelGraph, target_node: str, num_channels_to_close: int) -> [Channel]:
    closed_channels = []
    candidate_channels_to_close = []

    # Collect all candidate channels
    # We close only channels with nodes that have more than 1 channel already so we can correctly redestribute
    # their capacity and they don't remain disconnected from the graph
    for dest_node in G.get_connected_nodes(target_node):
        for ch in G.get_channels(target_node, dest_node):
            if len(G.network.out_edges(dest_node)) > 1:
                candidate_channels_to_close.append(ch)

    # Randomly shuffle the list of candidate channels
    random.shuffle(candidate_channels_to_close)

    # Iterate over the shuffled list and close channels
    for ch in candidate_channels_to_close:
        if len(closed_channels) < num_channels_to_close:
            if G.close_channel_bilateral(target_node, ch.dest, ch.short_channel_id):
                closed_channels.append(ch)
                ridistribute_capacity_of_closed_channel(G, ch.dest, ch)
            else:
                print(f'Channel from {ch.src[0:5]} --> {ch.dest[0:5]} - ID: {ch.short_channel_id} not closed...')
        else:
            break
    return closed_channels


def close_given_channels(G: ChannelGraph, target_node: str, channels_to_close: [Channel]):
    for i in range(len(channels_to_close)):
        if G.close_channel_bilateral(target_node, channels_to_close[i].dest, channels_to_close[i].short_channel_id):
            # print("channel closed correctly")
            ridistribute_capacity_of_closed_channel(G, channels_to_close[i].dest, channels_to_close[i])
        else:
            pass
            # print(f'channel given {channels_to_close[i].short_channel_id} not closed...')
    return True




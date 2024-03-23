import logging
import random
from src import ChannelGraph, Channel
from src.equilibrium_game.utils.obtain_capacity_from_channels import obtain_capacity_from_channels


def find_eligible_nodes(G, channel, all_nodes):
    """
    finds a new node to connect to that has degree > 2 and such that (1/2) * channel.capacity * 1/(deg+(new_node)) < min (c1, ..., cn) of the new_node
    :param G: channelGraph
    :param channel: channel
    :param all_nodes: set of all the nodes in the network
    :return: a list of nodes to which we can connect to
    """
    eligible_nodes = []
    for node in all_nodes:
        # Get all channels of the node B
        node_channels = G.get_all_channels_of_node(node)
        if node_channels:
            # Find the minimum capacity among the channels of node B

            min_capacity = min(ch.capacity for ch in node_channels)
            # (channel.capacity // 2) // len(G.network.out_edges(node)): is the liquidity to commit in the new channel
            # min_capacity is the minimum capacity among all the channels of the node to which we are connecting to
            if (len(node_channels) > 2) and ((channel.capacity // 2) // len(list(G.network.out_edges(node))) < min_capacity):
                # print(f'node {node[0:5]} eligible, opening channel of {channel.capacity} sats, we need ({channel.capacity} / {len(node_channels)}) from every channel,  min cap of {node[0:5]} is {min_capacity} > ({channel.capacity} / {len(node_channels)})')
                eligible_nodes.append(node)
    return eligible_nodes


def get_nodes_to_connect_to(G, channel, all_nodes):
    eligible_nodes = []

    for node in all_nodes:
        node_channels = G.get_all_channels_of_node(node)
        if node_channels:
            eligible_nodes.append(node)
    return eligible_nodes


def open_all_given_channels_randomly_NoEligibleNodes(G: ChannelGraph, target_node: str, channels_to_open: [Channel], opening_strategy) -> [Channel]:
    opened_channels = []
    all_nodes = set(G.network.nodes) - {target_node}
    for channel in channels_to_open:

        if opening_strategy == "SINGLE_FUNDED":
            # If the strategy is single funded the only requirement to the node we are connecting to
            # is that it has a out_degree > 1
            eligible_nodes = get_nodes_to_connect_to(G, channel, all_nodes)
            selected_node = random.choice(eligible_nodes)
            channel_created_chid = G.create_channel_bilateral(target_node, selected_node, channel.is_announced,
                                                              channel.capacity // 2,
                                                              channel.flags, channel.is_active, channel.last_update,
                                                              channel.base_fee,
                                                              channel.ppm, channel.cltv_delta, channel.htlc_min_msat,
                                                              channel.htlc_max_msat,
                                                              str(channel.short_channel_id) + '_2',
                                                              opposite_fee_mean=True)
            opened_channels.append(G.get_channel(target_node, selected_node, channel_created_chid))
        elif opening_strategy == "DUAL_FUNDED":
            # Instead if the strategy is dual funded the other requirement is that the channel we are connecting to
            # have enough capacity to provide to fund the new channel
            eligible_nodes = find_eligible_nodes(G, channel, all_nodes)


            # before creating the channel we have to get the liquidity from the channel we are connecting to
            if not eligible_nodes:
                # create the channel single funded
                eligible_nodes = get_nodes_to_connect_to(G, channel, all_nodes)
                selected_node = random.choice(eligible_nodes)
                channel_created_chid = G.create_channel_bilateral(target_node, selected_node, channel.is_announced, channel.capacity // 2, channel.flags, channel.is_active, channel.last_update, channel.base_fee, channel.ppm, channel.cltv_delta, channel.htlc_min_msat, channel.htlc_max_msat, str(channel.short_channel_id) + '_2', opposite_fee_mean=True)
                opened_channels.append(G.get_channel(target_node, selected_node, channel_created_chid))

            else:
                selected_node = random.choice(eligible_nodes)
                obtain_capacity_from_channels(G, selected_node, channel.capacity // 2)
                channel_created_chid = G.create_channel_bilateral(target_node, selected_node, channel.is_announced,
                                                                  channel.capacity,
                                                                  channel.flags, channel.is_active, channel.last_update,
                                                                  channel.base_fee,
                                                                  channel.ppm, channel.cltv_delta, channel.htlc_min_msat,
                                                                  channel.htlc_max_msat,
                                                                  str(channel.short_channel_id) + '_2',
                                                                  opposite_fee_mean=True)
                opened_channels.append(G.get_channel(target_node, selected_node, channel_created_chid))
    return opened_channels

def open_all_given_channels_randomly(G: ChannelGraph, target_node: str, channels_to_open: [Channel]) -> [Channel]:
    opened_channels = []
    used_nodes = set()

    # Function to find eligible nodes
    # Exclude the target node from the list of all nodes
    all_nodes = set(G.network.nodes) - {target_node}

    for channel in channels_to_open:
        eligible_nodes = find_eligible_nodes(G, channel, all_nodes)

        # Remove already used nodes if not all nodes have been used
        if len(used_nodes) < len(eligible_nodes):
            eligible_nodes = list(set(eligible_nodes) - used_nodes)
        else:
            # This means that I have used all the nodes that I could use so we start again picking nodes
            used_nodes.clear()
            eligible_nodes = find_eligible_nodes(G, channel, all_nodes)

        # If no eligible node is available
        if len(eligible_nodes) == 0:
            print("No eligible node found")
            channel_created_chid = G.create_channel_bilateral(target_node, channel.dest, channel.is_announced,
                                                              channel.capacity // 2,
                                                              channel.flags, channel.is_active, channel.last_update,
                                                              channel.base_fee,
                                                              channel.ppm, channel.cltv_delta, channel.htlc_min_msat,
                                                              channel.htlc_max_msat,
                                                              str(channel.short_channel_id) + '_2',
                                                              opposite_fee_mean=True)
            # print(f'|__OPENED OLD ch with {channel.dest[0:5]}, capacity: {channel.capacity // 2} ch_id: {channel.short_channel_id}_2')
            opened_channels.append(G.get_channel(target_node, channel.dest, channel_created_chid))
            continue

        selected_node = random.choice(eligible_nodes)
        used_nodes.add(selected_node)

        # Now that we have chosen the node to open the channel with we actually open the channel.
        # channel.capacity // 2 is the committed liquidity of the selected node
        # obtain_capacity_from_channels(G=G, node=selected_node, amt=channel.capacity // 2)

        channel_created_chid = G.create_channel_bilateral(target_node, selected_node, channel.is_announced,
                                                          channel.capacity // 2,
                                                          channel.flags, channel.is_active, channel.last_update,
                                                          channel.base_fee,
                                                          channel.ppm, channel.cltv_delta, channel.htlc_min_msat,
                                                          channel.htlc_max_msat,
                                                          str(channel.short_channel_id) + '_2',
                                                          opposite_fee_mean=True)
        # print(f'|__OPENED ch with {selected_node[0:5]}, capacity: {channel.capacity} ch_id: {channel.short_channel_id}_2')
        opened_channels.append(G.get_channel(target_node, selected_node, channel_created_chid))
        # logging.debug('opened ch with %s capacity: %d', selected_node, channel.capacity)

    return opened_channels

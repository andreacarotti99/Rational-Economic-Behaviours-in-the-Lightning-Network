import copy

from src.ChannelGraph import ChannelGraph


def replicate_node(channel_graph: ChannelGraph, node_to_copy: str, copier: str, duplicate_already_present_channel=True):
    channels_to_copy = []
    copier_neighbors_channels = []
    needed_liquidity = 0
    channels_to_close = []

    # getting all the channels to copy
    # copying all the channels that the highest capacity node doesn't already have

    # print('degree of the node to replicate is approximately: ', channel_graph.network.degree(node_to_copy) // 2)

    for neighbor in channel_graph.get_connected_nodes(node_to_copy):
        for ch in channel_graph.get_channels(src=node_to_copy, dest=neighbor):
            # if copier already has a channel towards the neighbor of node to copy
            # channels_to_copy.append(ch)
            needed_liquidity += ch.capacity // 2
            if channel_graph.network.has_edge(copier, ch.dest):
                # we add a tuple with true if the edge between copier and dest is already present, otherwise we add False
                channels_to_copy.append((ch, True))
            else:
                channels_to_copy.append((ch, False))

            # print(f"Added {ch} to channels_to_copy")

    # print()
    # closing channels up to amt needed
    deep_channels_to_copy = copy.deepcopy(channels_to_copy)

    for neighbor in channel_graph.get_connected_nodes(copier):
        for ch in channel_graph.get_channels(src=copier, dest=neighbor):
            copier_neighbors_channels.append(ch)

    reached_liquidity = 0
    for ch in copier_neighbors_channels:
        if ch.capacity // 2 + reached_liquidity > needed_liquidity:
            channels_to_close.append(ch)
            break
        reached_liquidity += ch.capacity // 2
        channels_to_close.append(ch)



    for i in range(len(channels_to_close)):
        # print(f'closing channel: {channels_to_close[i]}')
        channel_graph.close_channel_bilateral(src=channels_to_close[i].src, dest=channels_to_close[i].dest, short_channel_id=channels_to_close[i].short_channel_id)


    for ch, isAlreadyPresent in deep_channels_to_copy:
        if duplicate_already_present_channel:
            isAlreadyPresent = False

        if not isAlreadyPresent:
            channel_graph.create_channel_bilateral(
                source=copier,  # fixed
                dest=ch.dest,
                is_announced=ch.is_announced,
                total_capacity_of_channel=ch.capacity + 2,
                flags=ch.flags,
                is_active=ch.is_active,
                last_update= ch.last_update,
                base_fee=ch.base_fee - 1 if ch.base_fee > 0 else 0,
                ppm=ch.ppm - 1 if ch.ppm > 0 else 0,
                cltv_delta=ch.cltv_delta,
                htlc_min_msat=ch.htlc_min_msat,
                htlc_max_msat=ch.htlc_max_msat,
                channel_id=ch.short_channel_id + "_2",
                amount_sent= 10_000
            )

            # print(f'created channel: {ch.short_channel_id}_2')
        else:
            # if the edge from copier to node_to_copy neighbor is already present we close the channel and reopen with
            # increased capacity
            channelsAlreadyPresent = channel_graph.get_channels(copier, ch.dest)
            capacity_to_open = 0
            for channelAlreadyPresent in channelsAlreadyPresent:
                # print(f'channel {channelAlreadyPresent.short_channel_id} of {channelAlreadyPresent.capacity} already present btw {channelAlreadyPresent.src[0:5]} and {channelAlreadyPresent.dest[0:5]}')
                capacity_to_open += channelAlreadyPresent.capacity
                channel_graph.close_channel_bilateral(src=copier, dest=ch.dest, short_channel_id=channelAlreadyPresent.short_channel_id)

            # print(f'reopening a channel of size {capacity_to_open + ch.capacity} btw {copier[0:5]}... and {ch.dest[0:5]}...')
            channel_graph.create_channel_bilateral(
                source=copier,  # fixed
                dest=ch.dest,
                is_announced=ch.is_announced,
                total_capacity_of_channel=ch.capacity + 2 + capacity_to_open,
                flags=ch.flags,
                is_active=ch.is_active,
                last_update= ch.last_update,
                base_fee=ch.base_fee - 1 if ch.base_fee > 0 else 0,
                ppm=ch.ppm - 1 if ch.ppm > 0 else 0,
                cltv_delta=ch.cltv_delta,
                htlc_min_msat=ch.htlc_min_msat,
                htlc_max_msat=ch.htlc_max_msat,
                channel_id=ch.short_channel_id + "_2",
                amount_sent=10_000
            )
    print()

    # Closing all the channels of the node to copy
    node_to_copy_channels = []
    for neighbor in channel_graph.get_connected_nodes(node_to_copy):
        for ch in channel_graph.get_channels(src=node_to_copy, dest=neighbor):
            node_to_copy_channels.append(ch)
    for i in range(len(node_to_copy_channels)):
        # print(f'closing channel: {channels_to_close[i]}')
        channel_graph.close_channel_bilateral(src=node_to_copy_channels[i].src, dest=node_to_copy_channels[i].dest, short_channel_id=node_to_copy_channels[i].short_channel_id)

    '''
    for u, v, data in channel_graph.network.edges(data=True):
        if u == copier:
            print(data)
            print(data['channel'])
    '''
    return




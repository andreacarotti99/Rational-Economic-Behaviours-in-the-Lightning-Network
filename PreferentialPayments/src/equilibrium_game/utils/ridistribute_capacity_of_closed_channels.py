from src.Channel import Channel
from src.ChannelGraph import ChannelGraph


def ridistribute_capacity_of_closed_channel(G: ChannelGraph, node: str, closed_channel: Channel):
    total_cap_to_redistribute = closed_channel.capacity // 2
    if len(list(G.network.out_edges(node))) > 0:
        cap_for_each_edge = total_cap_to_redistribute // len(list(G.network.neighbors(node)))
        for dest_node in G.get_connected_nodes(node):
            for ch in G.get_channels(node, dest_node):
                G.close_channel_bilateral(node, dest_node, ch.short_channel_id)
                G.create_channel_bilateral(node,
                                           dest_node,
                                           ch.is_announced,
                                           ch.capacity + cap_for_each_edge,  # here is the edit
                                           ch.flags,
                                           ch.is_active,
                                           ch.last_update,
                                           ch.base_fee,
                                           ch.ppm,
                                           ch.cltv_delta,
                                           ch.htlc_min_msat,
                                           ch.htlc_max_msat,
                                           ch.short_channel_id,
                                           opposite_fee_mean=True)

    return

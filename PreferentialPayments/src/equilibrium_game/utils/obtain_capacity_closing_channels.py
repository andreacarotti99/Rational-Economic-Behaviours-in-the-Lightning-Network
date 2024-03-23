from src.ChannelGraph import ChannelGraph


def obtain_capacity_from_channels(G: ChannelGraph, node: str, amt: int):
    cap_for_each_edge_to_get = amt // len(list(G.network.out_edges(node)))

    print(f"amt: {amt}, cap to get: {cap_for_each_edge_to_get}")
    print(f"exp cap: {G.get_expected_capacity(node)}")

    if amt > G.get_expected_capacity(node):
        print(
            f"Node {node} has a capacity of {G.get_expected_capacity(node)} < {amt} I cannot open a channel with this node")
        return False
    for dest_node in G.get_connected_nodes(node):
        for ch in G.get_channels(node, dest_node):
            G.close_channel_bilateral(node, dest_node, ch.short_channel_id)
            print(f'updating ch {node[0:5]} --> {dest_node[0:5]} with capacity: {ch.capacity} - {cap_for_each_edge_to_get} = {ch.capacity - cap_for_each_edge_to_get}')
            G.create_channel_bilateral(node, dest_node, ch.is_announced,
                                       ch.capacity - cap_for_each_edge_to_get,  # here is the edit
                                       ch.flags, ch.is_active, ch.last_update, ch.base_fee, ch.ppm, ch.cltv_delta,
                                       ch.htlc_min_msat, ch.htlc_max_msat, ch.short_channel_id
                                       )
    return True


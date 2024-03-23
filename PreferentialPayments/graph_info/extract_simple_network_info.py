import os
from src.ChannelGraph import ChannelGraph
import numpy as np

path = '../snapshots/19jan2023_c-lightning.json'
channel_graph = ChannelGraph(path)

print('Number of nodes in the snapshot: ', channel_graph.network.number_of_nodes())
print('Number of (directed) edges in the snapshot: ', channel_graph.network.number_of_edges())

channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")
distinct_short_channel_ids = set()
total_capacity = 0
edges_with_zero_fee = 0
edges = 0

capacities = []
min_capacity = float('inf')
for u, v, k in channel_graph.network.edges(data=True):
    short_channel_id = k.get("chid")
    if k.get("fee") == 0:
        edges_with_zero_fee += 1
    edges += 1
    if short_channel_id is not None:
        if k.get('capacity') < min_capacity:
            min_capacity = k.get('capacity')
        distinct_short_channel_ids.add(short_channel_id)
        total_capacity += k.get("capacity")
        capacities.append(k.get("capacity"))

# Initialize a counter for nodes with all zero-fee channels
nodes_with_all_zero_fee_channels = 0

# Iterate over all nodes in the network
for node in channel_graph.network.nodes():
    # Get all outgoing edges for the node
    out_edges = channel_graph.network.out_edges(node, data=True)
    num_edges = len(out_edges)
    count = 0
    for u, v, k in out_edges:
        if k.get("fee") >= 0 and k.get("fee") < 2:
            count += 1
    if count == num_edges:
        nodes_with_all_zero_fee_channels += 1


print("Number of distinct short_channel_id:", len(distinct_short_channel_ids))
print("Total capacity:", total_capacity / 2)
print("Total Edges", edges)
print("Edges with 0 fee:", edges_with_zero_fee)
print("Nodes with all 0 fees:", nodes_with_all_zero_fee_channels)
print("Min capacity: ", np.min(capacities))
print("Mean capacity: ", np.mean(capacities))
print("Median capacity: ", np.median(capacities))

from path import snapshot_path
from src.ChannelGraph import ChannelGraph

path = snapshot_path
channel_graph = ChannelGraph(path)
channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")

G = channel_graph.network
min_capacity = float('inf')
min_edge = None

# Iterate over all edges
for edge in G.edges(data=True):
    capacity = edge[2]['capacity']
    if capacity < min_capacity:
        min_capacity = capacity
        min_edge = edge

# Iterate over all edges
count = 0
for edge in G.edges(data=True):
    capacity = edge[2]['capacity']
    if capacity < 100_000:
        count += 1
        min_edge = edge

print(f"The edge with the smallest capacity is {min_edge[0][0:5]}<--> {min_edge[1][0:5]} with a capacity of {min_capacity}")
print(f"Num of edges with capacity < 100_000: {count}")

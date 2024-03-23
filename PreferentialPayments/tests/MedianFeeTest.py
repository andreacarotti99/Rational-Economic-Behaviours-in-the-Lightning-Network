import numpy as np
from src.ChannelGraph import ChannelGraph
import path


channel_graph = ChannelGraph(path)
channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")
channel_graph.remove_edges_over_threshold(feature='fee', threshold=500)

fees = []
for u, v, k in channel_graph.network.edges(data=True):
    # print(k)
    fee = short_channel_id = k.get("fee")
    fees.append(fee)

# Create a NumPy array
arr = np.array(fees)
# Calculate mean
mean = np.mean(arr)
print(f"Mean fee: {mean}")

# Calculate median
median = np.median(arr)
print(f"Median fee: {median}")

import os
from src.ChannelGraph import ChannelGraph
import matplotlib.pyplot as plt

path ="../snapshots/19jan2023_c-lightning.json"
channel_graph = ChannelGraph(path)
channel_graph.transform_channel_graph_to_simpler(1000, "weighted_by_capacity")


G = channel_graph.network
node_degrees = {node: G.degree(node) for node in G.nodes()}
node_capacities = {node: channel_graph.get_expected_capacity(node) for node in G.nodes()}
sorted_nodes = sorted(node_degrees, key=node_degrees.get, reverse=True)
sorted_capacities = [node_capacities[node] for node in sorted_nodes]

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(range(len(sorted_capacities)), sorted_capacities)
plt.title("Node Capacities by Degree Rank", fontsize=20)
plt.ylabel("Capacity", fontsize=16)
plt.yscale('log')
plt.xlabel("Nodes (sorted by degree)", fontsize=16)
plt.grid(True)
plt.show()

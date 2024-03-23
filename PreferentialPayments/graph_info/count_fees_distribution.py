import os
import networkx as nx
import pandas as pd
from src.ChannelGraph import ChannelGraph

def save_to_csv_with_pandas(base_fee_counts, ppm_counts, filename):
    df = pd.DataFrame({
        'Range': [f"{r[0]}-{r[1]}" for r in base_fee_counts],
        'Base Fee Count': base_fee_counts.values(),
        'PPM Count': ppm_counts.values()
    })
    df.to_csv(filename, index=False)

def count_fee_ranges(network):
    # Define the ranges for counting
    ranges = [(0, 0), (1, 1), (2, 20), (21, 100), (101, 500), (501, 999), (1000, 1000), (1001, 10000), (10001, float('inf'))]
    base_fee_counts = {r: 0 for r in ranges}
    ppm_counts = {r: 0 for r in ranges}

    # Iterate over all edges in the network
    for _, _, edge_data in network.edges(data=True):
        base_fee = edge_data.get('base_fee', 0)
        ppm = edge_data.get('ppm', 0)

        # Count base_fee and ppm in their respective ranges
        for r in ranges:
            if r[0] <= base_fee <= r[1]:
                base_fee_counts[r] += 1
            if r[0] <= ppm <= r[1]:
                ppm_counts[r] += 1

    return base_fee_counts, ppm_counts


base_path ="YOUR_BASE_PATH"
path = os.path.join(base_path, 'PreferentialPayment 2/snapshots/19jan2023_c-lightning.json')
channel_graph = ChannelGraph(path)
channel_graph.transform_channel_graph_to_simpler(1000, "weighted_by_capacity")
G = channel_graph.network
count_fee_ranges(G)

base_fee_counts, ppm_counts = count_fee_ranges(G)
save_to_csv_with_pandas(base_fee_counts, ppm_counts, 'fee_counts.csv')
print('base fee:\n', base_fee_counts)
print('ppm:\n', ppm_counts)

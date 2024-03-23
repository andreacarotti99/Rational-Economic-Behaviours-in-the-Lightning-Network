import pandas as pd

from path import snapshot_path
from src.ChannelGraph import ChannelGraph


file = 'YOUR_BASE_PATH/PreferentialPayment 2/tests/first_part/results_100trans_10000SAT_0.1alfa_unifdist_1.csv'

# -------------------------------------------------------


df_original = pd.read_csv(file)
path = snapshot_path
channel_graph = ChannelGraph(path, 10_000)
channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")
network_nodes = channel_graph.network.nodes
existing_nodes = set(df_original['node'])

missing_nodes = []
missing_capacities = []
for i, node in enumerate(network_nodes):
    if node not in existing_nodes:
        missing_nodes.append(node)
        missing_capacities.append(channel_graph.get_expected_capacity(node))

df_missing = pd.DataFrame({
        'node': missing_nodes,
        'ratio': [0] * len(missing_nodes),
        'capacity': missing_capacities,
        'routed_payments': [0] * len(missing_nodes),
        'total_fee': [0] * len(missing_nodes)
    })

df = pd.concat([df_original, df_missing], ignore_index=True)
df['capacity'] = df['capacity'].astype(int)

df.to_csv('final_data.csv', index=False)

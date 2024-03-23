import networkx as nx
import pandas as pd
from src.ChannelGraph import ChannelGraph
from src.replicate_strategy_game.HBC.convertMultidigraphToDigraph import convert_multidigraph_to_digraph
from path import snapshot_path


channel_graph = ChannelGraph(snapshot_path)
channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")


alfa = 0.0
Graph = convert_multidigraph_to_digraph(channelGraph=channel_graph, alfa=alfa, amount_sent=10_000)
print("Computing betwenness centrality (edges weight: greedy weight )...")
bc_greedy_alfa = nx.betweenness_centrality(Graph, weight='greedy_weight', normalized=True)
df_bc_greedy = pd.DataFrame(list(bc_greedy_alfa.items()), columns=['node', f'bc_greedy_alfa{alfa}'])

df_bc_greedy_sorted = df_bc_greedy.sort_values(by=f'bc_greedy_alfa{alfa}', ascending=False)
df_bc_greedy_sorted.to_csv(f'bc_alfa{alfa}.csv', index=False)



'''
print("Computing betwenness centrality (edges weight: standard weight )...")
bc_standard = nx.betweenness_centrality(Graph, weight=1, normalized=True)
print(bc_standard)
df_bc_standard = pd.DataFrame(list(bc_standard.items()), columns=['node', 'bc_standard'])

print("Computing betwenness centrality (edges weight: fees)...")
bc_fee = nx.betweenness_centrality(Graph, weight='fee', normalized=True)
print(bc_fee)
df_bc = pd.DataFrame(list(bc_fee.items()), columns=['node', 'bc_fee'])

print("Computing betwenness centrality (edges weight: rev cap)...")
bc_reverse_capacity = nx.betweenness_centrality(Graph, weight='reverse_capacity', normalized=True)
df_reverse_capacity = pd.DataFrame(list(bc_reverse_capacity.items()), columns=['node', 'bc_reverse_capacity'])

df_merged = pd.merge(df_bc, df_reverse_capacity, on='node')
df_merged = pd.merge(df_merged, df_bc_standard, on='node')
gammas = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

for gamma in gammas:
    column_name = f'bc_gamma_{gamma}'  # Creates column names like bc_gamma_0, bc_gamma_2, etc.
    df_merged[column_name] = gamma * df_merged['bc_fee'] + (1 - gamma) * df_merged['bc_reverse_capacity']

# Now df_merged contains the original data plus the new bc_gamma columns
print(df_merged)

df_merged.to_csv('bc_gammas.csv', index=False)
print("Dataframe saved to 'bc_gammas.csv'")
'''


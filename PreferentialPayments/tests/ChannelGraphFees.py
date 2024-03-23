import numpy as np

from path import snapshot_path
from src.ChannelGraph import ChannelGraph
import pandas as pd

path = snapshot_path
channel_graph = ChannelGraph(path)
channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")


fees = []
for u, v, data in channel_graph.network.edges(data=True):
    fees.append(data['fee'])

print(fees)



int_series = pd.Series(fees)
int_count = int_series.value_counts()
int_count_df = int_count.reset_index()
int_count_df.columns = ['Integer', 'Count']
int_count_df.to_csv('integer_counts.csv', index=False)

# ------------------------------

int_series = pd.Series(fees)
bins = list(range(0, 501, 50))  # More granular buckets from 0 to 500 with a step of 50
bins += list(range(501, 10002, 500))
bins.append(np.inf)  # Adding a final bin for values > 10000
int_series_cut = pd.cut(int_series, bins, right=False)
bucket_counts = int_series_cut.value_counts().sort_index()
bucket_counts_df = bucket_counts.reset_index()
bucket_counts_df.columns = ['Bucket', 'Count']

# Save the DataFrame to a CSV file
# bucket_counts_df.to_csv('bucket_counts_extended.csv', index=False)



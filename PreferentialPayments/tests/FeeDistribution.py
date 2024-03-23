from path import snapshot_path
from src.ChannelGraph import ChannelGraph

from src.utils.normalize import *

path = snapshot_path
channel_graph = ChannelGraph(path)
channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")

capacities_list = [data['capacity'] for u, v, data in channel_graph.network.edges(data=True)]
fee_list = [(data['base_fee'] + data['ppm'] * 10_000 / 1000) for u, v, data in channel_graph.network.edges(data=True) if 4000 >= data['ppm'] > 10 and data['base_fee'] < 20_000]

print(f'max fee:  {max(fee_list)}')

import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(fee_list, kde=True)
plt.xlabel('Values')
plt.ylabel('Density')
plt.title('Density Plot of Data')
plt.show()

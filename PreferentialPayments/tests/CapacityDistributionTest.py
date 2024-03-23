from path import snapshot_path
from src.ChannelGraph import ChannelGraph
from src.utils.normalize import min_max_normalize
import math
import seaborn as sns
import matplotlib.pyplot as plt

path = snapshot_path
channel_graph = ChannelGraph(path, 10_000)
channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")

capacities_list = [data['capacity'] for u, v, data in channel_graph.network.edges(data=True)]
fee_list = [data['ppm'] for u, v, data in channel_graph.network.edges(data=True) if data['ppm'] <= 20_000]

max_capacity = max(capacities_list)
min_capacity = min(capacities_list)
capacities_list_normalized = [(min_max_normalize(data['capacity'], min_capacity, max_capacity)) for u, v, data in channel_graph.network.edges(data=True)]

l = []
for i in range(len(capacities_list_normalized)):
    try:
        l.append(-math.log(capacities_list_normalized[i]))
    except Exception:
        print('Capacity normalized: ', capacities_list_normalized[i])


sns.histplot(l, kde=True)
plt.xlabel('Values')
plt.ylabel('Density')
plt.title('Density Plot of Data')
plt.show()

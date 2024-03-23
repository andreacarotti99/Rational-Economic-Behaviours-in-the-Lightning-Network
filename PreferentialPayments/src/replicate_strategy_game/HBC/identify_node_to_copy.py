from src.ChannelGraph import ChannelGraph
from src.PathMap import PathMap
from src.replicate_strategy_game.utils.compute_bc_from_pathMap import compute_bc_from_pathMap
from src.utils.weight_function import weight_function_min_max
from path import snapshot_path

payments_to_simulate = 1000
payments_amount = 10_000
mu = 1000
base = 20_000
distribution = "uniform"
dist_func = ""
verbose = False
my_weight_function = weight_function_min_max
alfa = 0
# -------------------------------------------------------------------------------------

channel_graph = ChannelGraph(snapshot_path)
channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")

# the agent is the node who will decrease its capacity and copy the target node
agent = channel_graph.get_highest_capacity_nodes(1)[0]

# Compute the BC for all the nodes in the network
pathMap = PathMap(channel_graph=channel_graph, alfa=alfa, amount_sent=payments_amount, my_weight_function=my_weight_function)
# print(pathMap.map)
print('computing all nodes bc...')
all_nodes_bc_dict = compute_bc_from_pathMap(pathMap.map)

nodes = set(channel_graph.network.nodes)

# potential_targets is a set containing all the nodes that have capacity below half of the capacity of the agent node
potential_targets = {key for key, value in channel_graph.get_nodes_capacities().items() if value < channel_graph.get_expected_capacity(agent) // 2}

nodes_to_remove = {key for key, value in channel_graph.get_nodes_capacities().items() if value > channel_graph.get_expected_capacity(agent) // 2}


for node in nodes_to_remove:
    all_nodes_bc_dict.pop(node, None)

sorted_items_bc_dict = sorted(all_nodes_bc_dict.items(), key=lambda x: x[1])
node_with_highest_capacity_to_copy = sorted_items_bc_dict[-1][0]

print(sorted_items_bc_dict)

print("The agent node is:", agent)
print('capacity: ', channel_graph.get_expected_capacity(agent))
print()
print("The node with capacity with the highest value is:", node_with_highest_capacity_to_copy)
print('capacity: ', channel_graph.get_expected_capacity(node_with_highest_capacity_to_copy))

print(all_nodes_bc_dict)

# --------------------------------------------

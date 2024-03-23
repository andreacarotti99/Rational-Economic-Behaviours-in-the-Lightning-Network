import numpy as np

from src import ChannelGraph
from src.utils.computeDemand import f

def pick_target_node(channel_graph: ChannelGraph, strategy: str, tentative_nodes_to_keep: int, total_tests: int, already_chosen_nodes: [str]):
    if strategy == "random":
        target_node = channel_graph.get_random_node_uniform_distribution()

        # we check whether the number of neighbors of the target node is greater of the half of all the nodes in the network
        # if this is the case we need another target node because we cannot open the number of channels that we just closed
        while len(channel_graph.get_connected_nodes(target_node)) > (tentative_nodes_to_keep // 2):
            target_node = channel_graph.get_random_node_uniform_distribution()
        return target_node
    elif strategy == "capacity":
        highest_capacity_nodes = channel_graph.get_highest_capacity_nodes(n=total_tests*2)
        for node in highest_capacity_nodes:
            if node not in already_chosen_nodes and len(channel_graph.get_connected_nodes(node)) <= (tentative_nodes_to_keep // 2):
                already_chosen_nodes.append(node)
                return node
    else:
        print('The strategy provided does not exist!')
        exit()

def get_random_node_weighted_by_capacity(nodes_capacities: dict, dist_func_name: str):
    """
    Randomly chooses a key from a dictionary proportional to its value.
    Args: d (dict): A dictionary with numeric values.
    Returns: Any: A key from the dictionary chosen randomly, proportional to its value.
    """
    # Get the keys and values from the dictionary
    keys = list(nodes_capacities.keys())

    values = np.array([f(val, dist_func_name) for val in nodes_capacities.values()])
    # values = np.array(list(f(d.values())))
    # print(values)
    # Normalize the values to create a probability distribution
    probs = values / np.sum(values)
    # Use numpy's random.choice() method to choose a key from the dictionary
    random_key = np.random.choice(keys, p=probs)
    return random_key

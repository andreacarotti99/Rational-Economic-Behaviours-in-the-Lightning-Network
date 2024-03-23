import networkx as nx
import random


def pick_high_degree_nodes(graph, num_nodes=5, degree=2):
    # Create a list of nodes with degree higher than 2
    high_degree_nodes = [node for node, deg in graph.degree() if deg > degree]

    # Check if there are enough nodes with degree higher than 2
    if len(high_degree_nodes) < num_nodes:
        # Not enough nodes, return as many as possible or handle the case differently
        print(f"Not enough nodes with degree > 2. Only {len(high_degree_nodes)} nodes available.")
        return high_degree_nodes

    # Randomly select 'num_nodes' nodes from the list of high degree nodes
    return random.sample(high_degree_nodes, num_nodes)

def pick_nodes_of_degree_n(graph, min_degree=2):
    high_degree_nodes = [node for node, deg in graph.degree() if deg >= min_degree]
    return high_degree_nodes

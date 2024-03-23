import networkx as nx

from src.ChannelGraph import ChannelGraph
from src.utils.weight_function import weight_function_min_max


def convert_multidigraph_to_digraph(channelGraph: ChannelGraph, alfa: float, amount_sent: int):

    channelGraph.add_edge_property("alfa", alfa)
    channelGraph.add_edge_property("amount_sent", amount_sent)
    channelGraph.remove_edges_over_threshold(feature='fee', threshold=20_000)
    channelGraph.add_edge_property('max_fee', channelGraph.max('fee'))
    channelGraph.add_edge_property('max_cap', channelGraph.max('capacity'))
    G = channelGraph.network

    H = nx.DiGraph()


    # Iterate over edges in G
    for u, v, data in G.edges(data=True):
        # If the edge already exists in H, update the fee if it's lower
        if not H.has_edge(u, v):
            # Otherwise, add the edge to H with the current fee

            greedy_weight = weight_function_min_max(u, v, edge_data=G.get_edge_data(u, v))

            # print(data)
            H.add_edge(u, v,
                       fee=int(data['fee'])+1,
                       capacity=data['capacity'],
                       reverse_capacity=1000/data['capacity'],
                       greedy_weight= greedy_weight if greedy_weight > 0 else 1
                       )
    return H

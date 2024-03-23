import networkx as nx
from src import ChannelGraph
from src.utils.custom_dijkstra import custom_all_pairs_dijkstra
from src.utils.fee_function import *


class PathMap:

    def __init__(self, channel_graph: ChannelGraph, alfa: float, amount_sent: int, my_weight_function):
        self._alfa = alfa
        self._amount_sent = amount_sent
        self._channel_graph = channel_graph
        self._channel_graph.add_edge_property("alfa", alfa)
        self._channel_graph.add_edge_property("amount_sent", amount_sent)
        self._my_weight_function = my_weight_function

        # IMPORTANT: removing edges with fee over 20_000 msats because they are noise
        self._channel_graph.remove_edges_over_threshold(feature='fee', threshold=20_000)
        self._channel_graph.add_edge_property('max_fee', self._channel_graph.max('fee'))
        self._channel_graph.add_edge_property('max_cap', self._channel_graph.max('capacity'))

        print('Computing all pairs dijkstra in PathMap...')
        self._reverse_graph = self._channel_graph.network.reverse(copy=False)
        self._graph = self._channel_graph.network
        self._map = dict(custom_all_pairs_dijkstra(self._channel_graph.network.reverse(copy=False), weight=my_weight_function))
        print('Done all pairs dijkstra in PathMap')

    @property
    def map(self):
        return self._map
    @property
    def channel_graph(self):
        return self._channel_graph

    def print(self):
        for outer_key, inner_dict in self.map.items():
            print(f'from {outer_key}:')
            for inner_key, inner_list in inner_dict.items():
                print(f"  to {inner_key} path: {inner_list}")

    def get_path(self, src: str, dst: str):
        try:
            return self.map[src][dst]
        except KeyError:
            return []

    def get_cost_path(self, src: str, dst: str):
        return nx.shortest_path_length(self._graph, source=src, target=dst, weight=self._my_weight_function)

    def get_fee_path(self, src: str, dst: str):
        total = nx.shortest_path_length(self._graph, source=src, target=dst, weight=fee_function)
        return total


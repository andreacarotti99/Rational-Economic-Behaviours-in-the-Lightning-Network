import json
import random
from heapq import nlargest
import networkx as nx
import numpy as np
from src.Channel import Channel

class ChannelGraph:
    def __init__(self, lightning_cli_listchannels_json_file: str, amount_sent=10_000):
        self._snapshot_file = lightning_cli_listchannels_json_file
        self._channel_graph = nx.MultiDiGraph()
        channels = self._get_channel_json(lightning_cli_listchannels_json_file)
        self._channels = channels
        self._max_fee = None
        for channel in channels:
            channel = Channel(channel)
            self._channel_graph.add_edge(
                channel.src,
                channel.dest,
                key=channel.short_channel_id,
                channel=channel,
                ppm=channel.ppm,
                base_fee=channel.base_fee,
                capacity=channel.capacity,
                fee=(channel.ppm * (amount_sent / 1000)) + channel.base_fee,
                chid=channel.short_channel_id
            )
    def _get_channel_json(self, filename: str):
        f = open(filename)
        return json.load(f)["channels"]
    @property
    def network(self):
        return self._channel_graph

    @network.setter
    def network(self, new_network):
        self._channel_graph = new_network

    @property
    def max_fee(self):
        return self._max_fee
    @max_fee.setter
    def max_fee(self, max_fee):
        self._max_fee = max_fee
    @property
    def snapshot_file(self):
        return self._snapshot_file

    def get_channel(self, src: str, dest: str, short_channel_id: str) -> Channel:
        """
        returns a specific channel object identified by source, destination and short_channel_id
        from the ChannelGraph
        """
        if self.network.has_edge(src, dest):
            if short_channel_id in self.network[src][dest]:
                return self.network[src][dest][short_channel_id]["channel"]

    def get_channels(self, src: str, dest: str) -> [Channel]:
        """
        returns a list of channel objects identified by source, destination, for every short_channel_id
        from the ChannelGraph
        """
        result = []
        if self.network.has_edge(src, dest):
            for channel_id, channel_data in self.network[src][dest].items():
                result.append(channel_data["channel"])
            return result
        else:
            return []

    def get_channels_complete(self, src: str, dest: str) -> []:
        result = []
        if self.network.has_edge(src, dest):
            for channel_id, channel_data in self.network[src][dest].items():
                result.append(channel_data)
            return result
        else:
            return []

    def get_all_channels_of_node(self, node: str) -> [Channel]:
        """
        Returns a list of all channel objects associated with the given node in the ChannelGraph.
        """
        channels = []
        # Iterate over all edges (both incoming and outgoing) connected to the node
        for neighbor in self.network.neighbors(node):
            # In a MultiDiGraph, there can be multiple edges between two nodes
            for key in self.network[node][neighbor]:
                channel_data = self.network[node][neighbor][key]
                channels.append(channel_data["channel"])
        return channels

    def get_highest_capacity_nodes(self, n: int = 10) -> [str]:
        """
        :param n: number of highest capacity nodes to retrieve
        :return: a list of pub_key of the n highest capacity nodes
        """
        capacities = {}
        for src, dest, channel in self.network.edges(data="channel"):
            if src in capacities:
                capacities[src] += channel.capacity / 2
            else:
                capacities[src] = channel.capacity / 2
        top_nodes = nlargest(n, capacities, key=capacities.get)
        return top_nodes

    def transform_channel_graph_to_simpler(self, tentative_nodes_to_keep: int, strategy: str = "random"):
        """
        Takes as parameter the number of nodes we would like to have if it was just one strongly connected component,
        simplify the channelGraph by doing the following:
        1) takes the bigger strongly connected component in the network
        2) chooses according to the strategy tentative_nodes_to_keep nodes from the simplified network without replacement
        3) takes the subgraph obtained by those randomly selected nodes
        4) if in the subgraph obtained there is more than one strongly connected component keeps the largest one
        """
        # This is to get the bigger connected component in the network

        scc = list(nx.strongly_connected_components(self.network))  # get a list of the strongly connected components
        max_scc = max(scc, key=len)  # we select the biggest strongly connected component
        for c in scc:  # we iterate over the list of strongly connected components
            if c != max_scc:  # if c is not the biggest strongly connected component we remove the nodes in c from G
                self.network.remove_nodes_from(c)

        # This is to actually simplify the network
        nodes = list(self.network.nodes())
        if strategy == "weighted_by_capacity":
            # obtain a list of tentative_nodes_to_keep highest capacity nodes
            selected_nodes = self.get_highest_capacity_nodes(n=tentative_nodes_to_keep)
        elif strategy == "random":
            selected_nodes = np.random.choice(nodes, size=tentative_nodes_to_keep, replace=False)
        subgraph = self.network.subgraph(selected_nodes)
        connected_components = list(nx.strongly_connected_components(subgraph))
        largest_cc = subgraph.subgraph(max(connected_components, key=len))
        self.network = nx.MultiDiGraph(largest_cc)
        print(f"The network was modified and now has {largest_cc.number_of_nodes()} nodes")
        return

    def add_edge_property(self, property_name: str, property_value):
        """
        Add a property to every edge in the network graph.
        :param property_name: The name of the property to add.
        :param property_value: The value of the property to set.
        """
        for src, dest, edge_data in self.network.edges(data=True):
            if property_name not in edge_data:
                edge_data[property_name] = property_value

    def get_random_node_uniform_distribution(self):
        """
        returns a random node from the Network
        """
        if self.network.number_of_nodes() > 0:
            # random.seed(int(time.time() * 1000))
            return random.choice(list(self.network.nodes()))

    def get_nodes_capacities(self):
        """ compute the capacities for each node in the graph and returns a dictionary with the nodes and their capacity"""
        nodes_capacities = {}
        for src, dest, channel in self.network.edges(data="channel"):
            if src in nodes_capacities:
                nodes_capacities[src] += channel.capacity // 2
            else:
                nodes_capacities[src] = channel.capacity // 2
        return nodes_capacities

    def get_expected_capacity(self, node):
        try:
            capacity = self.get_nodes_capacities()[node]
            return capacity
        except KeyError:
            # print(f"Node {node} not found")
            return -1


    def remove_edges_below_threshold(self, feature: str, threshold: int):
        if feature == None:
            print('You must provide a feature to edit the graph!')
            exit()
        if feature == "capacity":
            edges = self._channel_graph.edges
            for edge in edges:
                # print(edge)
                edge_property = self._channel_graph.get_edge_data(edge[0], edge[1], edge[2])
                if edge_property['capacity'] < threshold:
                    print(f"Removing edge with capacity: {edge_property['capacity']}")
                    self._channel_graph.remove_edge(edge[0], edge[1], edge[2])
        return
    def get_connected_nodes(self, node):
        return list(self.network.successors(node))

    def close_channel_bilateral(self, src: str, dest: str, short_channel_id: str):
        """
        closes the channel btw src and dest given the short channel id
        """

        if self.network.has_edge(src, dest):
            if short_channel_id in self.network[src][dest]:
                self.network.remove_edge(src, dest, short_channel_id)
                self.network.remove_edge(dest, src, short_channel_id)
                # print(f"Closed edge between {src} and {dest}")
            return True
        else:
            # print(f"No edges between {src} and {dest}, 0 channels were closed")
            return False

    def close_all_channels(self, src: str, dest: str):
        """
        closes all the channels btw src and dest
        """
        if self.network.has_edge(src, dest):
            edge_keys = list(self.network[src][dest].keys())
            for edge_key in edge_keys:
                self.network.remove_edge(src, dest, edge_key)
                self.network.remove_edge(dest, src, edge_key)
        else:
            print(f"No edges between {src} and {dest}, 0 channels were closed")
        return


    def create_channel_bilateral(self, source, dest, is_announced, total_capacity_of_channel, flags, is_active, last_update,
                                 base_fee, ppm,
                                 cltv_delta, htlc_min_msat, htlc_max_msat, channel_id=None, amount_sent=10_000,
                                 opposite_fee_mean=False):

        """
        create a channel between two nodes (it is double sided the new channel created) so creates
        a channel A->B and also a channel B->A
        """
        if channel_id is None:
            channel_id = str(random.randint(100000, 999999)) + "x" + str(random.randint(1000, 9999)) + "x" + str(random.randint(1, 9))
        channel = {
            "source": str(source),
            "destination": str(dest),
            "short_channel_id": channel_id,
            "public": is_announced,
            "satoshis": total_capacity_of_channel,
            "amount_msat": str((total_capacity_of_channel) * 1000) + "msat",
            "message_flags": flags,
            "channel_flags": flags,
            "active": is_active,
            "last_update": last_update,
            "base_fee_millisatoshi": base_fee,
            "fee_per_millionth": ppm,
            "delay": cltv_delta,
            "htlc_minimum_msat": htlc_min_msat,
            "htlc_maximum_msat": htlc_max_msat,
            "features": ""
        }

        if opposite_fee_mean == True:
            fees = []
            for dest_neighbor in self.get_connected_nodes(dest):
                for ch in self.get_channels_complete(dest, dest_neighbor):
                    # print(ch)
                    fees.append(ch['fee'])
            if len(fees) > 0:
                # print(fees)
                median_fee = int(np.median(fees))
            else:
                median_fee = 10

        # print(f"Imposing {median_fee} as new fee")
        channel_rev = {
            "source": str(dest),
            "destination": str(source),
            "short_channel_id": channel_id,
            "public": is_announced,
            "satoshis": total_capacity_of_channel,
            "amount_msat": str((total_capacity_of_channel) * 1000) + "msat",
            "message_flags": flags,
            "channel_flags": flags,
            "active": is_active,
            "last_update": last_update,
            "base_fee_millisatoshi": base_fee if opposite_fee_mean is False else median_fee,
            "fee_per_millionth": ppm if opposite_fee_mean is False else 0,
            "delay": cltv_delta,
            "htlc_minimum_msat": htlc_min_msat,
            "htlc_maximum_msat": htlc_max_msat,
            "features": ""
        }
        channel = Channel(channel)
        channel_rev = Channel(channel_rev)
        # Adding the channel to the channelGraph
        self.network.add_edge(
            channel.src, channel.dest,
            key=channel.short_channel_id, channel=channel,
            ppm=channel.ppm,
            capacity=channel.capacity,
            base_fee=channel.base_fee,
            fee=(channel.ppm * (amount_sent / 1000)) + channel.base_fee,
            chid=channel.short_channel_id
            )
        self.network.add_edge(
            channel_rev.src, channel_rev.dest,
            key=channel_rev.short_channel_id,
            channel=channel_rev,
            ppm=channel_rev.ppm,
            capacity=channel_rev.capacity,
            base_fee=channel_rev.base_fee,
            fee=(channel_rev.ppm * (amount_sent / 1000)) + channel_rev.base_fee if opposite_fee_mean is False else median_fee,
            chid=channel.short_channel_id
            )
        return channel.short_channel_id

    def create_channel_bilateral_median_new_dest_fee(self, oldChannel: Channel, source: str, dest: str, amount_sent=10_000):
        """
        assuming payments of 10k sats, we can just put a base fee that corresponds to the one we want
        """

        channel = {"source": oldChannel.src, "destination": oldChannel.dest,
                   "short_channel_id": oldChannel.short_channel_id + "_2",
            "public": oldChannel.is_announced, "satoshis": oldChannel.capacity, "amount_msat": str((oldChannel.capacity) * 1000) + "msat",
            "message_flags": oldChannel.flags, "channel_flags": oldChannel.flags,
            "active": oldChannel.is_active, "last_update": oldChannel.last_update, "base_fee_millisatoshi": oldChannel.base_fee,
            "fee_per_millionth": oldChannel.ppm,
            "delay": oldChannel.cltv_delta, "htlc_minimum_msat": oldChannel.htlc_min_msat,
            "htlc_maximum_msat": oldChannel.htlc_max_msat, "features": ""
            }

        dest_channels = self.get_all_channels_of_node(dest)
        dest_channels_fees = []
        for ch in dest_channels:
            dest_channels_fees.append(ch['fee'])
        if len(dest_channels_fees) > 0:
            median_fee = np.median(dest_channels_fees)
        else:
            median_fee = 10

        oldChannelRev = self.get_channel(oldChannel.dest, oldChannel.src, oldChannel.short_channel_id)

        channel_rev = {"source": oldChannelRev.src, "destination": oldChannelRev.dest,
                       "short_channel_id": oldChannelRev.short_channel_id + "_2",
            "public": oldChannelRev.is_announced, "satoshis": oldChannelRev.capacity, "amount_msat": str((oldChannelRev.capacity) * 1000) + "msat",
            "message_flags": oldChannelRev.flags, "channel_flags": oldChannelRev.flags,
            "active": oldChannelRev.is_active, "last_update": oldChannelRev.last_update, "base_fee_millisatoshi": median_fee,
            "fee_per_millionth": 0,
            "delay": oldChannelRev.cltv_delta, "htlc_minimum_msat": oldChannelRev.htlc_min_msat,
            "htlc_maximum_msat": oldChannelRev.htlc_max_msat, "features": ""
            }

        channel = Channel(channel)
        channel_rev = Channel(channel_rev)

        self.network.add_edge(
            channel.src, channel.dest,
            key=channel.short_channel_id, channel=channel,
            ppm=channel.ppm,
            capacity=channel.capacity,
            base_fee=channel.base_fee,
            fee=(channel.ppm * (amount_sent / 1000)) + channel.base_fee,
            chid=channel.short_channel_id
            )
        self.network.add_edge(
            channel_rev.src, channel_rev.dest,
            key=channel_rev.short_channel_id,
            channel=channel_rev,
            ppm=channel_rev.ppm,
            capacity=channel_rev.capacity,
            base_fee=channel_rev.base_fee,
            fee=median_fee,
            chid=channel.short_channel_id
            )
        return channel.short_channel_id


    def open_channel_bilateral(self, channel_AB, channel_BA, amount_sent = 10_000):
        channel = Channel(channel_AB)
        channel_rev = Channel(channel_BA)
        # Adding the channel to the channelGraph
        self.network.add_edge(
            channel.src, channel.dest,
            key=channel.short_channel_id, channel=channel,
            ppm=channel.ppm,
            capacity=channel.capacity,
            base_fee=channel.base_fee,
            fee=(channel.ppm * (amount_sent / 1000)) + channel.base_fee,
            chid=channel.short_channel_id
            )
        self.network.add_edge(
            channel_rev.src, channel_rev.dest,
            key=channel_rev.short_channel_id,
            channel=channel_rev,
            ppm=channel_rev.ppm,
            capacity=channel_rev.capacity,
            base_fee=channel_rev.base_fee,
            fee=(channel_rev.ppm * (amount_sent / 1000)) + channel_rev.base_fee,
            chid=channel.short_channel_id
            )



    def remove_edges_over_threshold(self, feature: str, threshold: int, verbose=False):
        to_remove = []
        for edge in self.network.edges(data=True):
            # print(edge)
            if edge[2][feature] > threshold:
                to_remove.append(edge)
                if verbose:
                    print(f'Closing edge btw {edge[0]} and {edge[1]} with {feature} {edge[2][feature]} above {threshold}')
        for channel in to_remove:
            self.close_channel_bilateral(src=channel[0], dest=channel[1], short_channel_id=channel[2]['chid'])
        return


    def remove_edges_below_threshold(self, feature: str, threshold: int):
        to_remove = []
        for edge in self.network.edges(data=True):
            # print(edge)
            if edge[2][feature] < threshold:
                to_remove.append(edge)
                print(f'Closing edge with {feature} {edge[2][feature]} below {threshold}')
        for channel in to_remove:
            self.close_channel_bilateral(src=channel[0], dest=channel[1], short_channel_id=channel[2]['chid'])
        return


    def std_dev(self, feature: str):
        return np.std([data[feature] for u, v, data in self.network.edges(data=True)])

    def mean(self, feature: str):
        return np.mean([data[feature] for u, v, data in self.network.edges(data=True)])

    def max(self, feature: str):
        return np.max([data[feature] for u, v, data in self.network.edges(data=True)])

    def get_node_median_feature(self, node: str, feature: str):
        if node not in self.network:
            print(f"Node {node} not found in graph")
            return None
        edges = self.network.edges(node, data=True)
        weights = np.array([data.get(feature, 0) for _, _, data in edges])
        if len(weights) == 0:
            print(f"No edges connected to the node {node}")
            return None
        mean_weight = np.median(weights)
        return mean_weight

    def edit_channel(self, source: str, dest: str, short_channel_id, feature: str, new_value: int):
        '''
        ATTENTION:
        the object {'channel': <src.Channel.Channel object at 0x...>} doesn't change! (original channel data)

        :param feature: can be either fee, capacity, base_fee or ppm
        :param new_value: the new int value of the feature
        :return: True if the channel was successfully updated, False otherwise
        '''

        if self.network.has_edge(source, dest, short_channel_id):
            # print(self.network.get_edge_data(source, dest, short_channel_id))
            # channelObject = self.network.get_edge_data(source, dest, short_channel_id)['channel']
            # Attention in the edit we are just editing the fields of final fee (after computation of base and ppm)
            # and final capacity! we are not modifying the original fee in the fields of the channel
            # print(self.network[source][dest][short_channel_id])
            self.network[source][dest][short_channel_id][feature] = new_value
            # print(self.network[source][dest][short_channel_id])
            return True
        else:
            print(f'Channel {short_channel_id} not found')
            return False

    def remove_channel_attribute(self):
        for u, v, attributes in self.network.edges(data=True):
            if 'channel' in attributes:
                del attributes['channel']
        return






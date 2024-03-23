import copy
import sqlite3
from src.ChannelGraph import ChannelGraph
from src.Simulation import Simulation
from src.continuative_game.utils import queries
from src.continuative_game.utils.pick_high_degree_nodes import pick_high_degree_nodes
from src.equilibrium_game.utils.close_all_channels import close_all_channels
from src.equilibrium_game.utils.edit_all_channels import edit_randomly_all_channels
from src.continuative_game.params import *




def run_infinite_simulation(db: str, nodes_to_sample=5):

    channel_graph = ChannelGraph(snapshot_path)
    channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep, nodes_to_keep_strategy)
    channel_graph.remove_edges_over_threshold(feature='fee', threshold=path_cost_limit)
    print(f'Removed edges over {path_cost_limit} msats from the graph')
    params = (snapshot_path, payments_to_simulate, payments_amount, distribution, dist_func, tentative_nodes_to_keep, alfa, strategy_for_choosing_target_node, my_weight_function.__name__)

    # First simulation
    simulation_number = 0
    simulation_id = queries.db_insert_simulation_params(db, 'simulation', params)
    print('Simulation id: ', simulation_id)
    last_simulation = Simulation(channel_graph, payments_to_simulate, distribution, dist_func, alfa, payments_amount, my_weight_function, path_cost_limit)
    last_simulation.run()
    queries.db_insert_simulation_results(db, last_simulation, simulation_id, 0)
    simulation_number += 1

    while True:
        print(f'\nSimulation number: {simulation_number}')
        target_nodes = pick_high_degree_nodes(graph=channel_graph.network, num_nodes=nodes_to_sample, degree=2)

        old_graph_copy = copy.deepcopy(channel_graph)

        # List containing all the channels randomly opened of the nodes chosen
        all_nodes_edited_channels = []

        for i, node in enumerate(target_nodes):
            # print(f'Editing randomly channels of node {i}...')
            edited_channels = edit_randomly_all_channels(channel_graph, target_nodes[i], max_fee=250)
            # closed_channels = close_all_channels(channel_graph, target_nodes[i])
            # opened_channels = open_all_given_channels_randomly(channel_graph, target_nodes[i], closed_channels)
            all_nodes_edited_channels.append(edited_channels)

        penultimate_simulation = last_simulation

        del last_simulation
        last_simulation = Simulation(channel_graph, payments_to_simulate, distribution, dist_func, alfa,payments_amount, my_weight_function, path_cost_limit)
        last_simulation.run()
        queries.db_insert_simulation_results(db, last_simulation, simulation_id, simulation_number)

        # instead of going back to closing all the new channels opened and redistribute capacities correctly
        # we make a copy of the old graph and we reopen only those channels of nodes that allowed the nodes to earn more
        for i, node in enumerate(target_nodes):
            if last_simulation.get_ratio(node) > penultimate_simulation.get_ratio(node):
                print(f'node {i} with the new configuration earned more ({last_simulation.get_ratio(node)} > {penultimate_simulation.get_ratio(node)}) keeping its channels')
                edited_channels = all_nodes_edited_channels[i]


                for channel in edited_channels:
                    # Overwriting old fee with new fee in the nodes that had an improvement
                    print(f'overwritten in channel {channel.short_channel_id} old fee {old_graph_copy.network[channel.src][channel.dest][channel.short_channel_id]["fee"]} with {channel_graph.network[channel.src][channel.dest][channel.short_channel_id]["fee"]}')
                    old_graph_copy.network[channel.src][channel.dest][channel.short_channel_id]['fee'] = channel_graph.network[channel.src][channel.dest][channel.short_channel_id]['fee']
                    # close_all_channels(old_graph_copy, target_nodes[i])
                    # open_given_channels(old_graph_copy, node, opened_channels)
            else:
                print(f'node {i} with the new configuration earned less, reverting its old channels')
                # Don't do anything because the node in the new configuration earned more
                pass
        channel_graph = old_graph_copy
        simulation_number += 1
    return

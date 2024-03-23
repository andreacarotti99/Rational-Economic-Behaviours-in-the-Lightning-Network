import copy

from src.ChannelGraph import ChannelGraph
from src.Simulation import Simulation
from src.continuative_game.changing_both.utils.open_given_channels_with_new_fee import open_given_channels_with_new_fee
from src.continuative_game.params import *
from src.continuative_game.utils import queries
from src.continuative_game.utils.pick_high_degree_nodes import pick_nodes_of_degree_n
from src.equilibrium_game.utils.close_all_channels import close_randomly_n_channels, close_given_channels
from src.equilibrium_game.utils.open_given_channels import open_given_channels


def infinite_simulation(db):
    channel_graph = ChannelGraph(snapshot_path)
    channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep, nodes_to_keep_strategy)
    channel_graph.remove_edges_over_threshold(feature='fee', threshold=path_cost_limit)
    print(f'Removed edges over {path_cost_limit} millisatoshi from the graph')
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
        target_nodes = pick_nodes_of_degree_n(graph=channel_graph.network, min_degree=3)
        old_graph_copy = copy.deepcopy(channel_graph)

        all_nodes_opened_channels = []
        all_nodes_closed_channels = []

        for i, node in enumerate(target_nodes):
            closed_channels = close_randomly_n_channels(channel_graph, target_nodes[i], num_channels_to_close=1)
            all_nodes_closed_channels.append(closed_channels)
            opened_channels = open_given_channels_with_new_fee(channel_graph, target_nodes[i], closed_channels, opening_strategy, max_fee=250)
            all_nodes_opened_channels.append(opened_channels)

        penultimate_simulation = last_simulation
        del last_simulation
        last_simulation = Simulation(channel_graph, payments_to_simulate, distribution, dist_func, alfa, payments_amount, my_weight_function, path_cost_limit)
        last_simulation.run()
        queries.db_insert_simulation_results(db, last_simulation, simulation_id, simulation_number)

        for i, node in enumerate(target_nodes):
            if last_simulation.get_ratio(node) > penultimate_simulation.get_ratio(node):
                queries.update_increased_profit(db, simulation_id, simulation_number, node)
                print(f"Node {node[0:5]} profit is {last_simulation.get_ratio(node)} > {penultimate_simulation.get_ratio(node)} keeping new channels...")
                opened_channels = all_nodes_opened_channels[i]
                closed_channels = all_nodes_closed_channels[i]
                close_given_channels(old_graph_copy, target_nodes[i], closed_channels)

                # When we reopen we need to redit the channel as before
                open_given_channels(old_graph_copy, node, opened_channels)
                for channel in opened_channels:

                    try:
                        print(f'|__ overwritten in channel {channel.short_channel_id} old fee '
                              f'{old_graph_copy.network[channel.src][channel.dest][channel.short_channel_id]["fee"]} with '
                              f'{channel_graph.network[channel.src][channel.dest][channel.short_channel_id]["fee"]}')
                        old_graph_copy.network[channel.src][channel.dest][channel.short_channel_id]['fee'] = channel_graph.network[channel.src][channel.dest][channel.short_channel_id]['fee']

                    except Exception as e:
                        print(f"An error occurred: {e}")

            else:
                pass
        channel_graph = old_graph_copy
        simulation_number += 1
    return

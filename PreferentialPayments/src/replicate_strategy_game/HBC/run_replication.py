import copy
from src.ChannelGraph import ChannelGraph
from src.ExportResults import ExportResults
from src.Simulation import Simulation
from src.replicate_strategy_game.HRN.identify_HRN import *
from src.replicate_strategy_game.utils.replicate_node import replicate_node
from src.utils.weight_function import *
from path import snapshot_path



path = snapshot_path
payments_to_simulate = 1_000
distribution = 'uniform'
dist_func = ''
# alfa = 0.0
tentative_nodes_to_keep = 1000
payments_amount = 10_000
my_weight_function = weight_function_min_max
hrn_to_replicate = 10
duplicate_already_present_channel = True  # if false it increases the size of channels already present between the copier and the copied
# ----------------------------------------------------------------------------------------------------------------

alfas = [0.1]
high_cap_nodes = [11]  # these are the highest ratio nodes that in a simulation of 10k trans w. alfa=0.0 routed
# ----------------------------------------------------------------------------------------------------------------

def run_script(high_cap_node, alfa):

    bc_file_path = f"/../../../src/replicate_strategy_game/ConvexBC/data/bc_alfa{alfa}.csv"


    channel_graph = ChannelGraph(snapshot_path)
    channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=tentative_nodes_to_keep, strategy="weighted_by_capacity")


    # Run simulation 0
    simulation_0 = Simulation(channel_graph, payments_to_simulate, distribution, dist_func, alfa, payments_amount, my_weight_function)
    simulation_0.run()
    export = ExportResults(simulation_0)
    export_filename = export.export_results(simulation_number=str(0) + f"hcn{high_cap_node}_alfa{alfa}")

    agent = get_nth_hcn_from_results(export_filename, high_cap_node)
    # target = get_nth_hrn_from_results(export_filename, 1)

    target_idx = 0

    # Run the other simulations

    for i in range(hrn_to_replicate):
        simulation = None
        print(f"Replicating node {target_idx+1} in ranking")
        cg = copy.deepcopy(channel_graph)
        target = get_nth_highestBCnode_from_results(bc_file_path, target_idx+1, alfa=alfa)

        while cg.get_expected_capacity(agent) <= cg.get_expected_capacity(target):
            target_idx += 1
            target = get_nth_highestBCnode_from_results(bc_file_path, target_idx+1, alfa=alfa)
            if target_idx == 1000:
                print('no more nodes to check... exit')
                exit()
        target_idx += 1

        replicate_node(channel_graph=cg, node_to_copy=target, copier=agent, duplicate_already_present_channel=duplicate_already_present_channel)
        simulation = Simulation(cg, payments_to_simulate, distribution, dist_func, alfa, payments_amount, my_weight_function)
        simulation.run()
        export = ExportResults(simulation)
        export.export_results(simulation_number=str(i+1) + '_duplAlreadyPresent' + str(duplicate_already_present_channel) +
            "_hcn" + str(high_cap_node)
                              )
        print('old Ratio (simulation 0):\t', get_ratio_of_node(export_filename, agent))
        print(f'new Ratio (simulation {i+1}):\t', simulation.get_ratio(agent))


for high_cap_node in high_cap_nodes:
    print(f"Simulating hcn {high_cap_node}...")
    for alfa in alfas:
        print(f"Simulating using alfa = {alfa}")
        run_script(high_cap_node, alfa)


from src.utils.weight_function import *

# -- params -----------------------------

snapshot_path = "../../snapshots/19jan2023_c-lightning.json"
payments_to_simulate = 10_000
payments_amount = 10_000
distribution = "uniform"
dist_func = ""
tentative_nodes_to_keep = 1000
nodes_to_keep_strategy = "weighted_by_capacity"
total_tests = 201
alfa = 0.1  # alfa values that make sense: [0.01, 0.005, 0.001] bigger alfa means capacity more important
strategy_for_choosing_target_node = "random"
my_weight_function = weight_function_min_max
path_cost_limit = 500  # expressed in millisatoshi
nodes_to_sample = "ALL"  # can be 'ALL' or 20
opening_strategy = "SINGLE_FUNDED"  # or "DUAL_FUNDED"


def print_params():
    print(f'snapshot_path: {snapshot_path}')
    print(f'payments to simulate: {payments_to_simulate}')
    print(f'payments_amount: {payments_amount}')
    print(f'distribution: {distribution}')
    print(f'dist_func: {dist_func}')
    print(f'tentative_nodes_to_keep: {tentative_nodes_to_keep}')
    print(f'total_tests: {total_tests}')
    print(f'alfa: {alfa}')
    print(f'strategy for choosing target node: {strategy_for_choosing_target_node}')
    print(f'weight function: {my_weight_function.__name__}')
    print(f'Opening strategy: {opening_strategy}')
    if nodes_to_sample == "ALL":
        print(f'Nodes to sample per iteration: ALL')
    else:
        print(f'Nodes to sample per iteration: {nodes_to_sample}')
    print('-----------------------------------------------------')



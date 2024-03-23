from src.ChannelGraph import ChannelGraph
from src.ExportResults import ExportResults
from src.Simulation import Simulation
from src.utils.weight_function import *


BASE_PATH = "YOUR_BASE_PATH"
path = BASE_PATH + "PreferentialPayment/snapshots/cosimo_19jan2023_converted.json"
payments_to_simulate = 100
distribution = 'uniform'
dist_func = ''
alfa = 0.1
payments_amount = 10_000
my_weight_function = weight_function_min_max
tentative_nodes_to_keep = 1000

# ----------------------------------------------------------------------------------------------------------------

channel_graph = ChannelGraph(path)
channel_graph.transform_channel_graph_to_simpler(
    tentative_nodes_to_keep=tentative_nodes_to_keep,
    strategy="weighted_by_capacity")

simulation = Simulation(
    channel_graph,
    payments_to_simulate,
    distribution,
    dist_func,
    alfa,
    payments_amount,
    my_weight_function)
simulation.run()

export = ExportResults(simulation)
export.export_results()

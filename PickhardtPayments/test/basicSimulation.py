from pickhardtpayments.fork.ExportResults import ExportResults
from pickhardtpayments.fork.Simulation import Simulation
from pickhardtpayments.pickhardtpayments import ChannelGraph

base = 20_000
path = "../fork/SNAPSHOTS/19jan2023_c-lightning.json"
channel_graph = ChannelGraph(path)

channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")

simulation = Simulation(channel_graph=channel_graph, base=base)
simulation.run_success_payments_simulation(
            payments_to_simulate=10_000,
            payments_amount=10_000,
            mu=1,
            base=20_000,
            distribution="uniform",
            dist_func="",
            verbose=False,
            payments_amount_distribution="fixed"
        )
ER = ExportResults(simulation)
ER.export_results()

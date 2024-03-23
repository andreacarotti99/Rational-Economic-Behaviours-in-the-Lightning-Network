import pandas as pd
from src.Simulation import Simulation


class ExportResults(Simulation):
    def __init__(self, simulation: Simulation):
        self._simulation = simulation
        print("\n\nSaving results into dataframe...")
        df = pd.DataFrame(self._simulation.nodes_earning.items(), columns=['node', 'total_fee'])

        nodes = simulation.pathMap.channel_graph.network.nodes()
        all_nodes_df = pd.DataFrame({'node': list(nodes)})
        merged_df = pd.merge(all_nodes_df, df, on='node', how='left')
        merged_df.fillna({'total_fee': 0}, inplace=True)
        df = merged_df

        df['capacity'] = df['node'].map(self.simulation.pathMap.channel_graph.get_nodes_capacities())
        df['routed_payments'] = df['node'].map(self._simulation.nodes_routing)
        df['ratio'] = df['total_fee'] / df['capacity']

        df.fillna({'capacity': 0, 'routed_payments': 0, 'total_fee': 0, 'ratio': 0}, inplace=True)
        df = df[df['capacity'] != 0]

        self._results_df = df

    @property
    def simulation(self):
        return self._simulation

    def export_results(self, simulation_number: str = "1"):
        """
        Take a dataframe and exports it in the folder RESULTS as a csv file, the simulation number
        is used to distinguish between different simulation in the same run
        """
        s = self._simulation

        if s._dist_func == "":
            output_file = f"results_{str(s._num_of_payments)}trans_{s._amount_sent}SAT_{s._alfa}alfa_" \
                      f"{s._distribution[0:4]}dist_{simulation_number}"
        else:
            output_file = f"results_{str(s._num_of_payments)}trans_{s._amount_sent}SAT_{s._alfa}alfa_" \
                      f"{s._distribution[0:4]}dist_{s._dist_func}func_{simulation_number}"

        self._results_df.to_csv("%s.csv" % output_file, index=False)

        print(f"Results successfully exported to csv in file: {output_file}")
        return "%s.csv" % output_file

    def substitute_node_name(self, old_name, new_name):
        if old_name in self._results_df['node'].values:
            self._results_df.loc[self._results_df['node'] == old_name, 'node'] = new_name
        else:
            print(f"Node {old_name} not present in the dataframe, {new_name} was not set...")
        return




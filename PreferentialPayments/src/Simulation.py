import random
from collections import defaultdict
from tqdm import tqdm
from src.ChannelGraph import ChannelGraph
from src.utils.pick_node import get_random_node_weighted_by_capacity
from src.PathMap import PathMap
from src.utils.weight_function import weight_function_min_max


class Simulation:
    def __init__(self,
                channel_graph: ChannelGraph,
                num_of_payments: int, distribution: str, dist_func: str,
                alfa: float, amount_sent: int, my_weight_function=weight_function_min_max, path_cost_limit=500):
        self._pathMap = PathMap(channel_graph, alfa, amount_sent, my_weight_function)
        # print(my_weight_function.__name__)
        # print(self._pathMap.map)
        self._num_of_payments = num_of_payments
        self._distribution = distribution
        self._amount_sent = amount_sent
        self._alfa = alfa
        self._nodes_earning = {}
        self._nodes_routing = defaultdict(int)
        self._dist_func = dist_func
        self._failedPayments = 0
        self._path_cost_limit = path_cost_limit

    def payment(self, src: str, dst: str):
        self._assign_earnings(src=src, dst=dst)
    @property
    def pathMap(self):
        return self._pathMap
    @property
    def path_cost_limit(self):
        return self._path_cost_limit

    @property
    def failedPayments(self):
        return self._failedPayments

    def run(self):
        nodes = list(self.pathMap.channel_graph.network.nodes())
        nodes_capacities = self.pathMap.channel_graph.get_nodes_capacities()

        print(f"Simulating {self._num_of_payments} payments:")

        with tqdm(total=self._num_of_payments) as pbar:
            i = 0
            while i < self._num_of_payments:
                if self._distribution == "uniform":
                    src = random.choice(nodes)
                    dst = random.choice(nodes)
                    while src == dst:
                        dst = random.choice(nodes)
                elif self._distribution == "weighted_by_capacity":
                    src = get_random_node_weighted_by_capacity(nodes_capacities=nodes_capacities, dist_func_name=self._dist_func)
                    dst = get_random_node_weighted_by_capacity(nodes_capacities=nodes_capacities, dist_func_name=self._dist_func)
                    while src == dst:
                        dst = get_random_node_weighted_by_capacity(nodes_capacities=nodes_capacities, dist_func_name=self._dist_func)
                else:
                    print("Distribution not found! Exit...")
                    exit()
                # we have to swap sender and receiver because the fee from A to B to C is the one that
                # in a payment from A to C, B will earn depending on the value of the edge from B to A
                if self._assign_earnings(src=src, dst=dst):
                    pbar.update(1)
                    i += 1
                else:
                    self._failedPayments += 1
        return

    @property
    def nodes_earning(self):
        return self._nodes_earning

    @property
    def nodes_routing(self):
        return self._nodes_routing

    def _assign_earnings(self, src: str, dst: str):
        """

        :param src: source node of the payment
        :param dst: destination node of the payment
        :return: Boolean indicating whether the payment was successfull(True) or not (False)
        """

        path = self._pathMap.get_path(src, dst)
        # if the destination of the payment is a neighbor there is no cost
        if len(path) > 0:
            # Compute the cost of the path
            path_cost = 0
            for i in range(1, len(path)-1):
                path_cost += self._pathMap.get_fee_path(path[i-1], path[i])
            # Checking whether the cost of the path is less than the limit
            if path_cost > self._path_cost_limit:
                return False
            # Assigning the earnings to routing nodes
            for i in range(1, len(path)-1):
                # print(f'assigning cost {i}')
                if path[i] in self._nodes_earning:
                    self._nodes_earning[path[i]] += self._pathMap.get_fee_path(path[i-1], path[i])
                    self._nodes_routing[path[i]] += 1
                else:
                    self._nodes_earning[path[i]] = self._pathMap.get_fee_path(path[i-1], path[i])
                    self._nodes_routing[path[i]] = 1
            return True
        else:
            return False

    def get_ratio(self, node: str):
        if node in self.nodes_earning:
            return self.nodes_earning[node] / self.pathMap.channel_graph.get_expected_capacity(node)
        else:
            return 0

    def get_earning(self, node: str):
        if node in self.nodes_earning:
            return self.nodes_earning[node]
        else:
            return 0

from networkx import single_source_dijkstra_path
from tqdm import tqdm

def custom_all_pairs_dijkstra(G, cutoff=None, weight="weight"):

    path = single_source_dijkstra_path
    for n in tqdm(G):
        yield (n, path(G, n, cutoff=cutoff, weight=weight))

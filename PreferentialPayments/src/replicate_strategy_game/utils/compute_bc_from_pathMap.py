from collections import defaultdict


def compute_bc_from_pathMap(shortest_paths):
    '''

    :param shortest_paths: dict taken from PathMap
    :return: dictionary containing normalized BC
    '''
    # Initialize betweenness centrality dictionary
    betweenness_centralities = defaultdict(int)

    for s in shortest_paths:
        betweenness_centralities[s] = 0

    # Calculate betweenness centrality
    for s in shortest_paths:
        # print(f'from {s}')
        for t in shortest_paths[s]:
            # print(f'  to {t}')
            if s == t:
                continue
            # print('p:', shortest_paths[s][t])
            # Count how many shortest paths pass through each node
            for node in shortest_paths[s][t][1:-1]:
                betweenness_centralities[node] += 1

    # Normalize (optional, but common in many applications)
    n = len(shortest_paths)
    for node in betweenness_centralities:
        betweenness_centralities[node] = betweenness_centralities[node] / ((n - 1) * (n - 2))

    return betweenness_centralities

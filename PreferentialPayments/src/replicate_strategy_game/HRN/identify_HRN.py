import pandas as pd

def get_nth_hcn_from_results(results_path: str, hcn_rank_to_retrieve: int=1):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(results_path)
    # Sort the DataFrame by the 'ratio' column in descending order
    sorted_df = df.sort_values(by='capacity', ascending=False)
    # Get the 'pub_key' of the nth highest ratio row
    nth_cap_pub_key = sorted_df.iloc[hcn_rank_to_retrieve - 1]['node']
    print(f'highest cap node with rank {hcn_rank_to_retrieve}:\t\t', nth_cap_pub_key)
    return nth_cap_pub_key


def get_nth_hrn_from_results(results_path: str, hrn_rank_to_retrieve: int=1):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(results_path)
    # Sort the DataFrame by the 'ratio' column in descending order
    sorted_df = df.sort_values(by='ratio', ascending=False)
    # Get the 'pub_key' of the nth highest ratio row
    nth_highest_ratio_pub_key = sorted_df.iloc[hrn_rank_to_retrieve - 1]['node']
    print(f'highest ratio node with rank {hrn_rank_to_retrieve}:\t\t', nth_highest_ratio_pub_key)
    return nth_highest_ratio_pub_key

def get_nth_highestBCnode_from_results(results_path: str, highestBCnode_to_retrieve: int=1, alfa: int=-1):
    if alfa == -1:
        print("please provide working alfa to get_nth_highestBCnode_from_results()... exiting.")
    df = pd.read_csv(results_path)
    sorted_df = df.sort_values(by=f'bc_greedy_alfa{alfa}', ascending=False)
    nth_highest_BC_pub_key = sorted_df.iloc[highestBCnode_to_retrieve - 1]['node']
    print(f'highest BC node with rank {highestBCnode_to_retrieve}: \t\t', nth_highest_BC_pub_key)
    return nth_highest_BC_pub_key


def get_ratio_of_node(results_path: str, node_pub_key: str):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(results_path)
    # Find the row where the 'node' column matches the given node_pub_key
    node_row = df[df['node'] == node_pub_key]
    # If the node is not found, return a message
    if node_row.empty:
        print(f"Node with pub_key {node_pub_key} not found.")
        return None
    # Get the 'ratio' of that row
    node_ratio = node_row['ratio'].iloc[0]
    # print(f'Ratio of node with pub_key {node_pub_key}:\t\t', node_ratio)
    return node_ratio

def get_fees_of_node(results_path: str, node_pub_key: str):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(results_path)
    # Find the row where the 'node' column matches the given node_pub_key
    node_row = df[df['node'] == node_pub_key]
    # If the node is not found, return a message
    if node_row.empty:
        print(f"Node with pub_key {node_pub_key} not found.")
        return 0
    # Get the 'ratio' of that row
    node_ratio = node_row['total_fee'].iloc[0]
    # print(f'Ratio of node with pub_key {node_pub_key}:\t\t', node_ratio)
    return node_ratio


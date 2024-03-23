import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pickhardtpayments.pickhardtpayments import ChannelGraph

# Set display options for pandas
pd.set_option('display.max_columns', None)

# Define the data directory
data_dir = "../../fork/correlation/data/graphinfo.csv"
results_dir = ""


# Function to scale columns using MinMaxScaler
def scale_columns(dataframe, columns):
    scaler = MinMaxScaler()
    for col in columns:
        dataframe[col] = scaler.fit_transform(dataframe[[col]])
    return dataframe

# Read and scale node information
node_info_df = pd.read_csv(data_dir)
columns_to_scale = ['degree', 'degree_2_hops', 'exp_cap', 'avg_ppm', 'avg_base', 'median_ppm', 'median_base']
node_info_df = scale_columns(node_info_df, columns_to_scale)


# List of mu values
mu_values = [0, 1, 10, 100, 1000]


# Load graph from snapshot and transform
channel_graph = ChannelGraph("../../fork/SNAPSHOTS/19jan2023_c-lightning.json")
simpler_graph = channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")
myDiGraph = channel_graph.getDiGraph(amount=10_000, mu=1000)


for mu in mu_values:
    print(f'\n\nCorrelations for mu = {mu}')

    df_fees = pd.read_csv(results_dir)


    # Create a DataFrame with all nodes and merge with fees
    df_all_nodes = pd.DataFrame({'node': list(myDiGraph.nodes())})
    df_fees_complete = pd.merge(df_all_nodes, df_fees, how='left', on='node').fillna(0)

    # Merge the node info with fees
    df_final = pd.merge(df_fees_complete, node_info_df, how='inner', on='node')
    df_final.to_csv('test.csv')

    # Compute and print the Pearson correlation coefficients
    target_columns = ['ratio', 'total_fee']
    excluded_columns = target_columns + ['node', 'ROI', 'capacity']
    correlation_columns = [col for col in df_final.columns if col not in excluded_columns]

    print(f"{'Measure':<25}{'Correlation coefficient ratio':>37}{'Correlation coefficient fee':>38}")
    print("-" * 100)

    for column in correlation_columns:
        corr_coeff_ratio = df_final[column].corr(df_final['ratio'], method="spearman")
        corr_coeff_fee = df_final[column].corr(df_final['total_fee'], method="spearman")
        print(f"{column:<25}{corr_coeff_ratio:>25.4f}{corr_coeff_fee:>35.4f}")



import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from pickhardtpayments.pickhardtpayments import ChannelGraph

# Set the font to Times New Roman for all plots
plt.rcParams['font.family'] = 'Times New Roman'

# Function to read and preprocess data
def preprocess_data(data_dir, scaler):
    node_info_df = pd.read_csv(data_dir + 'graphinfo.csv')
    features_to_scale = ['degree', 'degree_2_hops', 'exp_cap', 'avg_ppm', 'avg_base', 'median_ppm', 'median_base']
    node_info_df[features_to_scale] = scaler.fit_transform(node_info_df[features_to_scale])
    return node_info_df

# Function to merge dataframes and fill NaN values
def merge_and_fill(df1, df2, key, fill_values):
    merged_df = pd.merge(df1, df2, how='left', on=key)
    for column, value in fill_values.items():
        merged_df[column] = merged_df[column].fillna(value)
    return merged_df

# Function to compute and print Pearson correlation
def compute_pearson_correlation(df, target_columns, exclude_columns):
    print(f"{'Measure':<25}{'Correlation coefficient ratio':>37}{'Correlation coefficient fee':>38}")
    print("-" * 100)
    for column in df.columns:
        if column not in target_columns and column not in exclude_columns:
            corr_coeffs = [df[column].corr(df[target], method='spearman') for target in target_columns]
            print(f"{column:<25}{corr_coeffs[0]:>25.4f}{corr_coeffs[1]:>35.4f}")

# Function to plot correlation heatmap
def plot_correlation_heatmap(df, drop_columns=None, fontsize=14):
    if drop_columns:
        df = df.drop(drop_columns, axis=1)
    corr_matrix = df.corr()
    mask = np.zeros_like(corr_matrix, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm')



    plt.xticks(fontsize=fontsize, rotation=45)
    plt.yticks(fontsize=fontsize)
    plt.show()

# Main script
def main():
    pd.set_option('display.max_columns', None)

    data_dir = "../../fork/predictingfees/data/"
    scaler = MinMaxScaler()

    node_info_df = preprocess_data(data_dir, scaler)

    df_fees = pd.read_csv(data_dir + 'labeled_results_10000trans_10000SAT_1000mu_distunif_amountdistfixe_1.csv')
    # df_fees = pd.read_csv(data_dir + 'results_10000trans_10000SAT_10mu__distweig_linear_amountsdistfixe_1.csv')

    channel_graph = ChannelGraph("../../fork/SNAPSHOTS/19jan2023_c-lightning.json")
    channel_graph.transform_channel_graph_to_simpler(tentative_nodes_to_keep=1000, strategy="weighted_by_capacity")
    myDiGraph = channel_graph.getDiGraph(amount=10_000, mu=1000)

    df_all_nodes = pd.DataFrame({'node': list(myDiGraph.nodes())})
    df_fees_complete = merge_and_fill(df_all_nodes, df_fees, 'node', {'ratio': 0, 'total_fee': 0})
    df_final = pd.merge(df_fees_complete, node_info_df, how='inner', on='node')
    df_final.to_csv('test.csv')

    print(df_final.columns)
    print()

    compute_pearson_correlation(df_final, ['ratio', 'total_fee'], ['node', 'ROI'])

    df_final.rename(columns=
                    {'exp_cap': 'Capacity',
                     'bc_pickhardt': 'BC Pickhardt',
                     'bc_capacity': 'BC 1/Capacity',
                     'degree': 'Degree',
                     'bc_standard': 'BC (w(e) = 1)',
                     'degree_2_hops': 'Degree-2',
                     'closeness_standard': 'Closeness C.',
                     'ec_standard': 'Eigenvector C.',
                     'ratio': 'Ratio',
                     'routed_payments': 'Routed Payments',
                     'total_fee': 'Fee earned',
                     'bc_ppm': 'BC PPM',
                     'bc_base': 'BC base fee'
                    }, inplace=True)

    plot_correlation_heatmap(df_final, drop_columns=['closeness_pickhardt','ec_pickhardt', 'capacity', 'avg_ppm', 'avg_base', 'median_ppm', 'median_base'])

if __name__ == "__main__":
    main()

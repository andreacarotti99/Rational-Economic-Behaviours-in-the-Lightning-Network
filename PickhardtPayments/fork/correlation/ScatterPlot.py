import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import networkx as nx
from pickhardtpayments.pickhardtpayments import ChannelGraph

# Set display options for pandas
pd.set_option('display.max_columns', None)

# Define the data directory

data_dir = "../../fork/correlation/data/graphinfo.csv"
results_file = ""


# Read node information and fees data from CSV files
node_info_df = pd.read_csv(data_dir)
df_fees = results_file



# Merge node information with fees data
df_fees_complete = pd.merge(node_info_df, df_fees, how='left', on='node')
df_fees_complete['ratio'] = df_fees_complete['ratio'].fillna(0)
df_fees_complete['total_fee'] = df_fees_complete['total_fee'].fillna(0)

# Sort the final dataframe
# Start with the original DataFrame
df_final = df_fees_complete.copy()

# Apply the first filter to remove rows with 'total_fee' equal to 0
df_final = df_final[df_final['total_fee'] > 0]

# Apply the second filter to remove rows with 'total_fee' greater than or equal to 500,000
df_final = df_final[df_final['total_fee'] < 500_000]

# Apply the third filter to remove rows with 'bc_pickhardt' greater than or equal to 0.1
df_final = df_final[df_final['bc_pickhardt'] < 0.1]

# Now df_final should only contain rows that meet all three conditions
# Verify the filters by checking the min and max of the columns
print(df_final['total_fee'].min(), df_final['total_fee'].max())
print(df_final['bc_pickhardt'].max())

# Scatter plot for 'bc_pickhardt' vs 'total_fee' after filtering
plt.scatter(df_final['bc_pickhardt'], df_final['total_fee'], s=5)
plt.title('Scatter Plot of Betweenness Centrality vs Total Fee (Filtered)')
plt.xlabel('Betweenness Centrality (scaled)')
plt.ylabel('Total Fee')
plt.grid(True)
plt.show()


#######


# Scatter plot for 'bc_pickhardt' vs 'total_fee' after filtering
plt.scatter(df_final['ec_standard'], df_final['total_fee'], s=5)
plt.title('Scatter Plot of Betweenness Centrality vs Total Fee (Filtered)')
plt.xlabel('Betweenness Centrality (scaled)')
plt.ylabel('Total Fee')
plt.grid(True)
plt.show()


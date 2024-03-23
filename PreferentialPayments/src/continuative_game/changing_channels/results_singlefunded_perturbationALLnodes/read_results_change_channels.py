import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Function to execute your query
from src.continuative_game.changing_channels.results_singlefunded_perturbation20nodes.queries_for_results import *

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11

def execute_query(db_path, query):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)

# Query for average fee up to SimulationNumber 200


# List of database paths
db_paths = [
            'channels_alfa0.0_unif_ALL.db',
            'channels_alfa0.001_unif_ALL.db',
            'channels_alfa0.1_unif_ALL.db',
            'channels_alfa0.0_weig_ALL.db',
            'channels_alfa0.001_weig_ALL.db',
            'channels_alfa0.1_weig_ALL.db',
            ]

legend_labels = {
    'channels_alfa0.0_unif_ALL.db': 'α = 0.0 - uniform distribution',
    'channels_alfa0.001_unif_ALL.db': 'α = 0.001 - uniform distribution',
    'channels_alfa0.1_unif_ALL.db': 'α = 0.1 - uniform distribution',

    'channels_alfa0.0_weig_ALL.db': 'α = 0.0 - capacity proportional',
    'channels_alfa0.001_weig_ALL.db': 'α = 0.001 - capacity proportional',
    'channels_alfa0.1_weig_ALL.db': 'α = 0.1 - capacity proportional',

}

color_map = {
    'channels_alfa0.0_unif_ALL.db': '#FF6347',    # Warm Color 1
    'channels_alfa0.001_unif_ALL.db': '#FFA07A',  # Warm Color 2
    'channels_alfa0.1_unif_ALL.db': '#FFD700',    # Warm Color 3

    'channels_alfa0.0_weig_ALL.db': '#87CEFA',    # Warm Color 1
    'channels_alfa0.001_weig_ALL.db': '#20B2AA',  # Warm Color 2
    'channels_alfa0.1_weig_ALL.db': '#6495ED',    # Warm Color 3

}



# Create a figure with two subplots
plt.figure(figsize=(15, 7.5))
max_simulation_number = 1000
# Loop through each database file and execute both queries
for i, db_path in enumerate(db_paths, start=1):
    # Execute avg fee query
    df_avg_fee = execute_query(db_path, avgFee_query(max_simulation_number=max_simulation_number))
    plt.subplot(1, 2, 1)
    plt.plot(df_avg_fee['SimulationNumber'], df_avg_fee['AvgFee'], label=legend_labels[db_path], color=color_map[db_path], alpha=0.75, zorder=3)

    # Execute avg fee for top 200 nodes query
    df_top200 = execute_query(db_path, increased_profit(max_simulation_number=max_simulation_number, group_size=1))
    plt.subplot(1, 2, 2)
    plt.plot(df_top200['SimulationGroup'], df_top200['TotalIncreasedProfit'], label=legend_labels[db_path], color=color_map[db_path], alpha=0.75, zorder=3)
    label = legend_labels[db_path]



# Plot settings for the first subplot
plt.subplot(1, 2, 1)
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5, zorder=2)
plt.xlabel('Simulation Number', fontsize=18)
plt.ylabel('Mean Fee (msat)', fontsize=18)
# Adjust legend for the first subplot with each entry on a new line
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=2)

# Plot settings for the second subplot

plt.subplot(1, 2, 2)
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5, zorder=2)
plt.xlabel('Simulation Number', fontsize=18)
plt.ylabel('# Nodes with increased profit vs previous simulation', fontsize=15)
# Adjust legend for the second subplot with each entry on a new line
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=2)



# Adjust the layout
plt.tight_layout(pad=3.0)
plt.subplots_adjust(wspace=0.3)  # Adjust this value as needed, smaller values reduce the space

plt.show()

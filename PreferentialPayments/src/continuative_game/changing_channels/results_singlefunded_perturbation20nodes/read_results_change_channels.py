import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from src.continuative_game.changing_channels.results_singlefunded_perturbation20nodes.queries_for_results import *

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11

def execute_query(db_path, query):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)


# List of database paths
db_paths = ['channels_alfa0.0_unif_20.db',
            'channels_alfa0.001_unif_20.db',
            'channels_alfa0.1_unif_20.db']

legend_labels = {
    'channels_alfa0.0_unif_20.db': 'α = 0.0 - uniform distribution - channel',
    'channels_alfa0.001_unif_20.db': 'α = 0.001 - uniform distribution - channel',
    'channels_alfa0.1_unif_20.db': 'α = 0.1 - uniform distribution - channel',
}

color_map = {
    'channels_alfa0.0_unif_20.db': '#FF6347',    # Warm Color 1
    'channels_alfa0.001_unif_20.db': '#FFA07A',  # Warm Color 2
    'channels_alfa0.1_unif_20.db': '#FFD700',    # Warm Color 3

    # 'fees_alfa0.0_weig.db': '#87CEFA',  # Cold Color 4
    # 'fees_alfa0.001_weig.db': '#20B2AA',  # Cold Color 5
    # 'fees_alfa0.1_weig.db': '#6495ED'    # Cold Color 6
}



plt.figure(figsize=(14, 7))
max_simulation_number = 1000
group_size = 100

for i, db_path in enumerate(db_paths, start=1):
    # Execute avg fee query
    df_avg_fee = execute_query(db_path, avgFee_query(max_simulation_number=max_simulation_number))
    plt.subplot(1, 2, 1)
    plt.plot(df_avg_fee['SimulationNumber'], df_avg_fee['AvgFee'], label=legend_labels[db_path], color=color_map[db_path])

    # Execute avg fee for top 200 nodes query
    df_top200 = execute_query(db_path, increased_profit(max_simulation_number=max_simulation_number, group_size=group_size))
    plt.subplot(1, 2, 2)
    plt.plot(df_top200['SimulationGroup'], df_top200['TotalIncreasedProfit'], label=legend_labels[db_path], color=color_map[db_path])
    label = legend_labels[db_path]



# Plot
plt.subplot(1, 2, 1)
plt.title('Mean Fee per Simulation')
plt.xlabel('Simulation Number', labelpad=15)
plt.ylabel('Mean Fee (msats)', fontsize=14)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=2)

plt.subplot(1, 2, 2)
plt.title('Sum of Nodes Showing Profit Increase in Each Simulation\nCompared to the Previous, Grouped in Sets of 10 Simulations')
plt.xlabel('Simulation Set (Each Set Contains 100 Simulations)')
plt.ylabel('Cumulative Count of Nodes with Increased Profit', fontsize=14)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=2)
plt.tight_layout(pad=3.0)
plt.show()

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Function to execute your query
from src.continuative_game.changing_fees.results_perturbation20nodes import *
from scipy.interpolate import make_interp_spline
import numpy as np


from src.continuative_game.utils.queries_for_results import *

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11

def execute_query(db_path, query):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)

# Query for average fee up to SimulationNumber 200


# List of database paths
db_paths = [
    'fees_alfa0.0_unif_ALL.db', 'fees_alfa0.001_unif_ALL.db', 'fees_alfa0.1_unif_ALL.db',
    'fees_alfa0.0_weig_ALL.db', 'fees_alfa0.001_weig_ALL.db', 'fees_alfa0.1_weig_ALL.db']

legend_labels = {
    'fees_alfa0.0_unif_ALL.db': 'α = 0.0 - uniform',
    'fees_alfa0.001_unif_ALL.db': 'α = 0.001 - uniform',
    'fees_alfa0.1_unif_ALL.db': 'α = 0.1 - uniform',
    'fees_alfa0.0_weig_ALL.db': 'α = 0.0 - capacity proportional',
    'fees_alfa0.001_weig_ALL.db': 'α = 0.001 - capacity proportional',
    'fees_alfa0.1_weig_ALL.db': 'α = 0.1 - capacity proportional'

}

color_map = {
    'fees_alfa0.0_unif_ALL.db': '#FF6347',    # Warm Color 1
    'fees_alfa0.001_unif_ALL.db': '#FFA07A',  # Warm Color 2
    'fees_alfa0.1_unif_ALL.db': '#FFD700',    # Warm Color 3
    'fees_alfa0.0_weig_ALL.db': '#87CEFA',  # Cold Color 4
    'fees_alfa0.001_weig_ALL.db': '#20B2AA',  # Cold Color 5
    'fees_alfa0.1_weig_ALL.db': '#0323f5'    # Cold Color 6
}


max_simulation_number = 1000
group_size = 100

# Create a figure with two subplots
plt.figure(figsize=(14, 7))




# Loop through each database file and execute both queries
for i, db_path in enumerate(db_paths, start=1):
    # Execute avg fee query


    df_avg_fee = execute_query(db_path, avgFee_query(max_simulation_number=max_simulation_number))
    plt.subplot(1, 2, 1)
    plt.grid(True, linestyle='--', color='grey', linewidth=0.5, alpha=0.5)
    plt.plot(df_avg_fee['SimulationNumber'], df_avg_fee['AvgFee'], label=legend_labels[db_path], color=color_map[db_path], alpha=0.75)


    # Execute avg fee for top 200 nodes query
    df_top200 = execute_query(db_path, increased_profit(max_simulation_number=max_simulation_number, group_size=group_size))
    plt.subplot(1, 2, 2)
    plt.grid(True, linestyle='--', color='grey', linewidth=0.5, alpha=0.5)
    # plt.grid(True, linestyle='--', alfa=0.6)
    plt.plot(df_top200['SimulationGroup'], df_top200['TotalIncreasedProfit'], label=legend_labels[db_path], color=color_map[db_path], alpha=0.75)
    label = legend_labels[db_path]








# Plot settings for the first subplot
plt.subplot(1, 2, 1)
# plt.title('Mean Fee per Simulation')
plt.xlabel('Simulation Number', labelpad=15, fontsize=18)
plt.ylabel('Mean Fee (msat)', fontsize=18)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.24), fancybox=True, shadow=True, ncol=2)
plt.subplot(1, 2, 2)
max_simulation_number = (df_top200['SimulationGroup'].max() + 1) * group_size
# print(df_top200)
# print(max_simulation_number)

# IF GROUP SIZE IS SET
if group_size > 1:
    num_labels = (max_simulation_number + group_size - 1) // group_size  # Calculate the number of labels needed
    tick_labels = [f'[{i*group_size+1}-{(i+1)*group_size}]' for i in range(num_labels)]
    tick_positions = range(num_labels)  # Positions for the labels
    plt.xticks(tick_positions, tick_labels, rotation=30, ha='right')


# tick_labels = ['1-20', '21-40', '41-60', '61-80', '81-100', '101-120', '121-140', '141-160', '161-180', '181-200']
# tick_positions = range(0, 10)  # Assuming each label corresponds to a group number starting from 1

# plt.title(f'Sum of Nodes Showing Profit Increase in Each Simulation\nCompared to the Previous, Grouped in Sets of {group_size} Simulations')
# plt.xlabel(f'Simulation Bucket (Each bucket Contains {group_size} Simulations)', labelpad=15, fontsize=18)
if group_size == 1:
    plt.xlabel(f'Simulation Number', labelpad=15, fontsize=18)
else:
    plt.xlabel(f'Simulation Group', labelpad=15, fontsize=18)

if group_size == 1:
    plt.ylabel(f'# Nodes with increased profit vs previous simulation', fontsize=14)
else:
    plt.ylabel(f'# Nodes with increased profit vs previous simulation\nin groups of {group_size} simulations', fontsize=14)

# Adjust legend for the second subplot with each entry on a new line
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.24), fancybox=True, shadow=True, ncol=2)

plt.tight_layout(pad=3.0)

plt.show()





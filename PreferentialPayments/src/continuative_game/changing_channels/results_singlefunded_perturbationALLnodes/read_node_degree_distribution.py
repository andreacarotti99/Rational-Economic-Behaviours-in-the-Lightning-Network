import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from src.continuative_game.changing_channels.results_singlefunded_perturbation20nodes.queries_for_results import *

# Function to execute your query
def execute_query(db_path, query):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11

# List of database paths
db_paths = [
    'channels_alfa0.0_unif_ALL.db',
    'channels_alfa0.001_unif_ALL.db',
    'channels_alfa0.1_unif_ALL.db']

# Specific simulation numbers to plot
simulation_numbers_to_plot = [0, 100, 500, 1000]

# Create a figure for the plots
n_dbs = len(db_paths)
n_sims = len(simulation_numbers_to_plot)
plt.figure(figsize=(15, 7.5))  # Adjust the figure size as needed

axes = []
bars = []
# Loop through each database file and plot
for i, db_path in enumerate(db_paths, start=1):
    df_degree_dist = execute_query(db_path, node_degree_dist())

    for j, sim_number in enumerate(simulation_numbers_to_plot, start=1):
        ax = plt.subplot(n_dbs, n_sims, (i - 1) * n_sims + j)
        axes.append(ax)
        subset = df_degree_dist[df_degree_dist['SimulationNumber'] == sim_number]

        degree_counts = subset['Node_channels'].value_counts().sort_index()

        # print(degree_counts)

        plt.grid(axis='y', alpha=0.5, linestyle='--', zorder=0)
        plt.grid(axis='y', alpha=0.5, linestyle='--', zorder=0)

        # Plot a bar chart with node degrees on the y-axis and frequencies on the x-axis
        if i == 1:
            bar = plt.bar(degree_counts.index, degree_counts.values, alpha=0.75, color='#FF6347', edgecolor='#B8252A', linewidth=0.8, zorder=3)
        elif i == 2:
            bar = plt.bar(degree_counts.index, degree_counts.values, alpha=0.75, color='#FFA07A', edgecolor='#E89020', linewidth=0.8, zorder=3)
        else:
            bar = plt.bar(degree_counts.index, degree_counts.values, alpha=0.75, color='#FFD700', edgecolor='#DEC20B', linewidth=0.8, zorder=3)

        bars.append(bar[0])


        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        if i == 1:
            plt.title(f'Simulation Number: {sim_number}', fontsize=18, loc='center', y=1.3)
        if j == 1:
            plt.ylabel('Frequency', fontsize=16)
        plt.xlabel('# Node Channels', fontsize=16)
        legend_title = 'α = ' + f'{db_path.split("_")[1]}'[4:] + '\n      -\nUniform'

        if j == 4:
            axes[-1].legend([bars[-1]], [legend_title], loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=False, ncol=1,
                            fontsize='large')


        # plt.legend(loc='upper right', )
        # plt.legend(loc='best', fancybox=True, shadow=False, ncol=3, title=legend_title)

        plt.xticks(range(0, 51, 10), fontsize='13')

        plt.ylim(0, 110)
        plt.xlim(0, 50)

# Adjust the layout
plt.tight_layout(pad=3.0)

plt.show()

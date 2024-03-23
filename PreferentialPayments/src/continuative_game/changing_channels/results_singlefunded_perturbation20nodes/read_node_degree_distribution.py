import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from src.continuative_game.changing_channels.results_singlefunded_perturbation20nodes.queries_for_results import *

def execute_query(db_path, query):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)

db_paths = ['channels_alfa0.0_unif.db', 'channels_alfa0.001_unif.db', 'channels_alfa0.1_unif.db']

# Specific simulation numbers to plot
simulation_numbers_to_plot = [0, 50, 100, 200]

# Create a figure for the plots
n_dbs = len(db_paths)
n_sims = len(simulation_numbers_to_plot)
plt.figure(figsize=(15, 7.5))  # Adjust the figure size as needed

# Loop through each database file and plot
for i, db_path in enumerate(db_paths, start=1):
    df_degree_dist = execute_query(db_path, node_degree_dist())

    for j, sim_number in enumerate(simulation_numbers_to_plot, start=1):
        plt.subplot(n_dbs, n_sims, (i - 1) * n_sims + j)
        subset = df_degree_dist[df_degree_dist['SimulationNumber'] == sim_number]

        degree_counts = subset['Node_channels'].value_counts().sort_index()

        # Plot a bar chart with node degrees on the y-axis and frequencies on the x-axis
        plt.bar(degree_counts.index, degree_counts.values, alpha=0.8)

        plt.title(f'{db_path.split("_")[1]}: Simulation {sim_number}')
        plt.ylabel('Node Channels (Degree)')
        plt.xlabel('Frequency')

        plt.ylim(0, 90)
        plt.xlim(0, 60)

plt.tight_layout(pad=3.0)
plt.show()

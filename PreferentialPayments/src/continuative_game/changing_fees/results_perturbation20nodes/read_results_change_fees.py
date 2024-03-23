import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from src.continuative_game.changing_channels.results_singlefunded_perturbation20nodes.queries_for_results import \
    avgFee_query, increased_profit

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11

def execute_query(db_path, query):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)



# List of database paths
db_paths = ['fees_alfa0.0_unif.db',
            'fees_alfa0.001_unif.db',
            'fees_alfa0.1_unif.db',
            'fees_alfa0.0_weig.db',
            'fees_alfa0.001_weig.db',
            'fees_alfa0.1_weig.db']

legend_labels = {
    'fees_alfa0.0_unif.db': 'α = 0.0 - uniform distribution',
    'fees_alfa0.001_unif.db': 'α = 0.001 - uniform distribution',
    'fees_alfa0.1_unif.db': 'α = 0.1 - uniform distribution',
    'fees_alfa0.0_weig.db': 'α = 0.0 - capacity proportional',
    'fees_alfa0.001_weig.db': 'α = 0.001 - capacity proportional',
    'fees_alfa0.1_weig.db': 'α = 0.1 - capacity proportional'

}

color_map = {
    'fees_alfa0.0_unif.db': '#FF6347',    # Warm Color 1
    'fees_alfa0.001_unif.db': '#FFA07A',  # Warm Color 2
    'fees_alfa0.1_unif.db': '#FFD700',    # Warm Color 3
    'fees_alfa0.0_weig.db': '#87CEFA',  # Cold Color 4
    'fees_alfa0.001_weig.db': '#20B2AA',  # Cold Color 5
    'fees_alfa0.1_weig.db': '#6495ED'    # Cold Color 6
}


# Create a figure with two subplots
plt.figure(figsize=(12, 7.5))

# Loop through each database file and execute both queries
for i, db_path in enumerate(db_paths, start=1):
    # Execute avg fee query
    df_avg_fee = execute_query(db_path, avgFee_query())
    plt.subplot(1, 2, 1)
    plt.plot(df_avg_fee['SimulationNumber'], df_avg_fee['AvgFee'], label=legend_labels[db_path], color=color_map[db_path])

    # Execute avg fee for top 200 nodes query
    df_top200 = execute_query(db_path, increased_profit())
    plt.subplot(1, 2, 2)
    plt.plot(df_top200['SimulationGroup'], df_top200['TotalIncreasedProfit'], label=legend_labels[db_path], color=color_map[db_path])
    label = legend_labels[db_path]



# Plot settings for the first subplot
plt.subplot(1, 2, 1)
plt.title('Mean Fee per Simulation')
plt.xlabel('Simulation Number', labelpad=15)
plt.ylabel('Mean Fee', fontsize=14)
# Adjust legend for the first subplot with each entry on a new line
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=2)

# Plot settings for the second subplot
plt.subplot(1, 2, 2)
tick_labels = ['1-20', '21-40', '41-60', '61-80', '81-100', '101-120', '121-140', '141-160', '161-180', '181-200']
tick_positions = range(0, 10)  # Assuming each label corresponds to a group number starting from 1
plt.xticks(tick_positions, tick_labels, rotation=45, ha='right')
plt.title('Sum of Nodes Showing Profit Increase in Each Simulation\nCompared to the Previous, Grouped in Sets of 10 Simulations')
plt.xlabel('Simulation Set (Each Set Contains 20 Simulations)')
plt.ylabel('Cumulative Count of Nodes with Increased Profit', fontsize=14)
# Adjust legend for the second subplot with each entry on a new line
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=2)

# Adjust the layout
plt.tight_layout(pad=3.0)

plt.show()





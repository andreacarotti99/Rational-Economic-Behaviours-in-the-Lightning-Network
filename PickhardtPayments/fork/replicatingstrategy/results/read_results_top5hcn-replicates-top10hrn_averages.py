import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import sem, t
from numpy import mean

# Set the global font to be Times New Roman, size 10
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 10

# Base directory containing the files
base_dir = "../../../fork/replicatingstrategy/results/HRN/top5hcn-replicates-top10hrn"

# Function to calculate average fees and confidence intervals
def calculate_average_fees_and_confidence(mu, num_hcns=5, confidence=0.95):
    fees_list = []
    for i in range(1, num_hcns+1):
        file_name = f"results_HRN_sats10000_numpayments1000_mu{mu}_distunif_tentnodes1000_closingrandom_hcn{i}.csv"
        file_path = os.path.join(base_dir, file_name)
        df = pd.read_csv(file_path)
        fees_list.append([df["old_fees"].iloc[0]] + df["new_fees"].tolist())

    # Calculate the average fees across all HCNs
    fees_array = np.array(fees_list)
    average_fees = np.mean(fees_array, axis=0)

    return average_fees

# Set up a figure for the subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 7))  # Only two subplots

# Define colors
darker_red = "#ff584f"
darker_green = "#5bb450"
pastel_blue = "#99ccff"

# Iterate over the two values of µ to create average plots
for index, mu in enumerate([1000, 10]):
    # Calculate average fees and confidence intervals
    average_fees = calculate_average_fees_and_confidence(mu)

    # Select the subplot
    ax = axs[index]

    # Set aspect ratio to make plots square
    ax.set_aspect(aspect='auto', adjustable='box')

    # Set y-axis to logarithmic scale
    ax.set_yscale('log')

    # Create a ranking list
    ranking = ['Before'] + [f"HRN {x+1}" for x in range(10)]

    # Plot bar graph for average fees with confidence intervals
    bars = ax.bar(ranking, average_fees, capsize=5, width=0.6, label=f"µ={mu}")

    # Color bars based on comparison with the reference fee
    for bar_index, bar in enumerate(bars):
        bar.set_color(pastel_blue if bar_index == 0 else (darker_green if average_fees[bar_index] >= average_fees[0] else darker_red))

    # Set x-axis labels
    ax.set_xticks(range(len(ranking)))
    ax.set_xticklabels(ranking, rotation=45, ha="center")

    ax.set_title(f"Average Fees for µ={mu}")
    ax.set_ylabel("Fees (log scale)")
    ax.legend()

# Adjust layout to fit everything
plt.tight_layout()
plt.show()

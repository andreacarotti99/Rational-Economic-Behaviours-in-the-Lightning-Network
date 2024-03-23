import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Set the global font to be Times New Roman, size 10
rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = 10

# Base directory containing the files
base_dir = "../../fork/replicatingstrategy/results/HRN/top5hcn-replicates-top10hrn"

# Set up a figure for the subplots
fig, axs = plt.subplots(2, 5, figsize=(20, 7))  # Adjusted figure size for square plots

# Define colors
darker_red = "#ff584f"
darker_green = "#5bb450"
pastel_blue = "#99ccff"  # For the first bar

# Iterate over the files, changing the order of µ to have µ=1000 on the first row
for row, mu in enumerate([1000, 10]):
    for col in range(5):
        i = col + 1  # HCN index
        file_name = f"results_HRN_sats10000_numpayments1000_mu{mu}_distunif_tentnodes1000_closingrandom_hcn{i}.csv"
        file_path = os.path.join(base_dir, file_name)

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Select the subplot
        ax = axs[row, col]

        # Set aspect ratio to make plots square
        ax.set_aspect(aspect='auto', adjustable='box')

        # Set y-axis to logarithmic scale
        ax.set_yscale('log')

        # Reference fee value from the "old_fees" column
        ref_fee = df["old_fees"].iloc[0]

        # Insert the old_fee as the first element in the new_fees column for plotting
        fees = [ref_fee] + df["new_fees"].tolist()

        # Create a new ranking list with an extra element for the old_fee
        ranking = ['Before'] + [f"HRN {x+1}" for x in df["ranking"]]

        # Plot bar graph for fees with thinner bars
        bars = ax.bar(ranking, fees, width=0.6, label=f"HCN{i}\nµ={mu}")  # Adjusted bar width

        # Color bars based on comparison with the reference fee
        for index, bar in enumerate(bars):
            if index == 0:  # First bar
                bar.set_color(pastel_blue)
            else:
                bar.set_color(darker_green if fees[index] >= ref_fee else darker_red)

        # Draw a thinner vertical grey line to distinguish the first bar
        ax.axvline(x=0.5, color='grey', linestyle='--', linewidth=1)

        # Set x-axis labels
        ax.set_xticks(range(len(ranking)))
        ax.set_xticklabels(ranking, rotation=45, ha="center", fontsize=14)  # Font size is set globally

        ax.set_title(f"Fees for HCN{i}", fontsize=16)
        ax.set_ylabel("Fees (log scale)", fontsize=17)
        # Increase legend font size and set to Times New Roman
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize=14, ncol=3)

# Adjust layout to fit everything
plt.tight_layout()
plt.subplots_adjust(hspace=0.6, wspace=0.4)  # Increased vertical and horizontal spacing
plt.show()




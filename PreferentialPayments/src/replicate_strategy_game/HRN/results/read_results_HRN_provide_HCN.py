import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Set 'Times New Roman' as the default font for all text in the plot
matplotlib.rcParams['font.family'] = 'Times New Roman'

# Base directory containing the folders
base_dir = "closing channels randomly 1000 trans hcn 1 - 11 - 13 - 21 - 27 - 28"

# Set up a figure for the subplots
fig, axs = plt.subplots(2, 5, figsize=(20, 7))  # Adjusted figure size for square plots

# Define colors
darker_red = "#ff584f"
darker_green = "#5bb450"
pastel_blue = "#99ccff"  # For the first bar

# Iterate over the folders and files
hcns = [1, 11, 13, 27, 28]

plot_index = 0
for hcn in hcns:
    for alfa in ["alfa0.0", "alfa0.1"]:
        # Replace 'alfa' with Greek letter 'α' and maintain the numeric part
        alfa_label = alfa.replace("alfa", "α = ")

        hcn_folder = f"hcn{hcn}"
        file_path = os.path.join(base_dir, hcn_folder, alfa, f"fees_and_delta_hcn{hcn}_{alfa}.csv")

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Select the subplot
        ax = axs[plot_index % 2, plot_index // 2]

        # ax.set_yscale('log')

        # Set aspect ratio to make plots square
        ax.set_aspect(aspect='auto', adjustable='box')

        # Reference fee value from the first bar
        ref_fee = df["Fees"].iloc[0]

        # Plot bar graph for Fees with thinner bars
        bars = ax.bar(df["Simulation"].astype(str), df["Fees"], width=0.6, label=f"HCN {hcn}\n{alfa_label}")  # Use the updated alfa_label

        # Color bars based on comparison with the reference fee
        for index, (bar, fee) in enumerate(zip(bars, df["Fees"])):
            if index == 0:  # First bar
                bar.set_color(pastel_blue)
                bar.set_edgecolor('navy')
            else:
                bar.set_color(darker_green if fee >= ref_fee else darker_red)
                bar.set_edgecolor('green' if fee >= ref_fee else '#8B0000')

        # Draw a thinner vertical grey line to distinguish the first bar
        ax.axvline(x=0.5, color='grey', linestyle='--', linewidth=1)

        # Set x-axis labels
        x_labels = [f"HRN {x}" if x != 0 else "Before" for x in df["Simulation"]]
        ax.set_xticks(df["Simulation"])
        ax.set_xticklabels(x_labels, rotation=45, ha="center", fontsize=14)  # Font size for x-axis labels

        # ax.set_title(f"Fees for HCN{hcn} {alfa_label}", fontsize=16)

        if plot_index == 0 or plot_index == 1:
            ax.set_ylabel("Fees (msat)", fontsize=19)

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize=14, ncol=3)  # Legend above the chart

        plot_index += 1

# Adjust layout to fit everything
plt.tight_layout()
plt.subplots_adjust(hspace=0.6, wspace=0.2)  # Increased vertical and horizontal spacing
plt.show()

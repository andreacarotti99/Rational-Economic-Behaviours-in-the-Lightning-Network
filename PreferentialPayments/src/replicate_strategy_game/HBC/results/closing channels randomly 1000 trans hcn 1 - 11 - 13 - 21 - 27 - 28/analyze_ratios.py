import pandas as pd

# Initialize the DataFrame to store the results
from src.replicate_strategy_game.HRN.identify_HRN import get_nth_hcn_from_results, get_fees_of_node

df_output = pd.DataFrame(columns=['Simulation', 'Fees', 'Delta (%)'])

# ------------------------------------------------------------------------------------

# Base path to the results
base_path = "/src/replicate_strategy_game/ConvexBC/results/closing channels randomly 1000 trans hcn 1 - 11 - 13 - 21 - 27 - 28/"
alfa = 0.1
hcn_rank_to_consider = 28

# ------------------------------------------------------------------------------------

# Function to generate the file path for a given simulation index
def generate_file_path(sim_index, hcn_rank, alfa_value):
    if sim_index == 0:
        # Special case for simulation 0
        return f"{base_path}hcn{hcn_rank}/alfa{alfa_value}/results_1000trans_10000SAT_{alfa_value}alfa_unifdist_0hcn{hcn_rank}_alfa{alfa_value}.csv"
    else:
        # General case for other simulations
        return f"{base_path}hcn{hcn_rank}/alfa{alfa_value}/results_1000trans_10000SAT_{alfa_value}alfa_unifdist_{sim_index}_duplAlreadyPresentTrue_hcn{hcn_rank}.csv"

# Get the highest capacity node (hcn)
hcn = get_nth_hcn_from_results(results_path=generate_file_path(0, hcn_rank_to_consider, alfa), hcn_rank_to_retrieve=hcn_rank_to_consider)

# Get the fees of the highest capacity node for the first simulation
fees_sim_0 = get_fees_of_node(generate_file_path(0, hcn_rank_to_consider, alfa), hcn)
print(f'Fees for sim 0: \t{fees_sim_0}')

df_output = df_output.append({'Simulation': 0, 'Fees': fees_sim_0, 'Delta (%)': 0}, ignore_index=True)

# Loop through the other simulations to get the fees and calculate the deltas
for i in range(1, 11):
    # Generate the file path for the ith simulation
    file_path_sim_i = generate_file_path(i, hcn_rank_to_consider, alfa)

    # Get the fees for the ith simulation
    fees_sim_i = get_fees_of_node(file_path_sim_i, hcn)
    print(fees_sim_i)

    # Calculate the delta in percentage

    delta = ((fees_sim_i - fees_sim_0) / fees_sim_0) * 100


    # Print the results
    print(f'Fees for sim {i}: \t{fees_sim_i}, \tDelta: {delta}%')

    # Append the results to the DataFrame
    df_output = df_output.append({'Simulation': i, 'Fees': fees_sim_i, 'Delta (%)': delta}, ignore_index=True)

# Convert 'Simulation' column to int type
df_output['Simulation'] = df_output['Simulation'].astype(int)

# Save the DataFrame to a new CSV file
output_file_name = f"fees_and_delta_hcn{hcn_rank_to_consider}_alfa{alfa}.csv"
df_output.to_csv(output_file_name, index=False)
print(f"Output saved to {output_file_name}")

import pandas as pd

# Load the path of your final_data CSV file
file_path = 'YOUR_BASE_PATH/PreferentialPayment 2/tests/first_part/final_data.csv'
new_file_name = 'bucketed_data.csv'

# ------------------------------------

df = pd.read_csv(file_path)
df['capacity'] = df['capacity'].astype(int)
df_sorted = df.sort_values(by='capacity', ascending=False).reset_index()
df_sorted['bucket_id'] = df_sorted.index // 200

# Group by the bucket ID and calculate the mean for the specified columns
df_grouped = df_sorted.groupby('bucket_id').agg({
    'ratio': 'mean',
    'routed_payments': 'mean',
    'total_fee': 'mean',
    'capacity': 'mean'
}).reset_index()

# Save the new DataFrame to a new CSV file
df_grouped.to_csv(new_file_name, index=False)

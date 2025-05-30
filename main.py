import os
import process_data
import pandas as pd


# Check if the directory exists
data = 'raw_data'

if not os.path.exists(data):
    print(f"Directory {data} does not exist.")
else:
    print(f"Directory {data} exists. Proceeding with data processing...")

data_df = pd.DataFrame()
# Iterate through all Excel files in the directory
for filename in os.listdir(data):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(data, filename)
        print(f"Processing file: {file_path}")
        # Read the Excel file
        test = filename.split('-')[1]
        test_level = filename.split('-')[5]  # Extracting the test level from the filename
        # print(test_level)
        data_df = process_data.process_pat(file_path, test, test_level, data_df)

    else:
        print(f"Skipping non-Excel file: {filename}")

# Output Data
data_df.to_csv('pat_data.csv')
import os
import process_data
import pandas as pd

### MATHS DATA PROCESSING ###
final_df = pd.DataFrame()
maths_data_dir = 'raw_data\\maths'
# Check if the directory exists
if not os.path.exists(maths_data_dir):
    print(f"Directory {maths_data_dir} does not exist.")
else:
    print(f"Directory {maths_data_dir} exists. Proceeding with data processing...")

# Iterate through all Excel files in the directory
for filename in os.listdir(maths_data_dir):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(maths_data_dir, filename)
        print(f"Processing file: {file_path}")
        # Read the Excel file
        test_level = filename.split('-')[5]  # Extracting the test level from the filename
        # print(test_level)
        final_df = process_data.process_pat_m(file_path, test_level, final_df)

    else:
        print(f"Skipping non-Excel file: {filename}")

final_df.to_clipboard()
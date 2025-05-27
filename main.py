import pandas as pd

patM = pd.read_excel('raw_data\\maths\\pat-maths-4th-edition-test-10-26052025-114014.xlsx')

# Remove the first 3 rows
patM = patM.iloc[3:]
# Reset the index
patM.reset_index(drop=True, inplace=True)

# print(patM)

# Find the index of the row where the first column is 'Unique ID'
header_index = patM[patM.iloc[:, 0] == 'Unique ID'].index[0]

# Slice all rows starting from the header row
patM_responses = patM.iloc[header_index:].reset_index(drop=True)
# Set the first row as header
patM_responses.columns = patM_responses.iloc[0]
# Remove the header row from the DataFrame data
patM_responses = patM_responses.iloc[1:]

# Remove columns, Family name, Given name, Middle name, Username, DOB, Gender, Year level (current), Active tags, Inactive tags, Tags (at time of test)
patM_responses = patM_responses.drop(columns=['Family name', 'Given name', 'Middle names', 'Username', 'DOB', 'Gender', 'Year level (current)', 'Year level (at time of test)', 'Active tags', 'Inactive tags', 'Tags (at time of test)'])

# Change the column names after Completed and before Score using their index positions

columns_list = list(patM_responses.columns)
completed_index = columns_list.index("Completed")
score_index = columns_list.index("Score")

# Loop through the columns between Completed and Score and set new names
for i in range(completed_index + 1, score_index):
    columns_list[i] = str(i - completed_index)  # numeric names starting at 1 as string

patM_responses.columns = columns_list

# Define the columns to keep
id_vars = ['Unique ID', 'Completed', 'Score', 'Scale', 'Stanine', 'Percentile']
# All remaining columns will be pivoted; these become the "QuestionNumber" column
value_vars = [col for col in patM_responses.columns if col not in id_vars]

# Melt the DataFrame so that the question columns are consolidated
patM_melted = pd.melt(patM_responses, 
                      id_vars=id_vars, 
                      value_vars=value_vars, 
                      var_name='QuestionNumber', 
                      value_name='Response')

# Convert Response values: NA becomes blank, ✓ becomes True, and all other values become False
patM_melted['Response'] = patM_melted['Response'].apply(
    lambda x: "" if pd.isna(x) else (True if x == '✓' else False)
)

patM_melted.to_clipboard()

print(patM_melted)


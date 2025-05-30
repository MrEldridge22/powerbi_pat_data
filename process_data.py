import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

def process_pat(excel_file, test, test_level, df):
    # Read the Excel file
    patData = pd.read_excel(excel_file, header=None)
    
    # Remove the first 3 rows
    patData = patData.iloc[3:]
    # Reset the index
    patData.reset_index(drop=True, inplace=True)

    ### Get Question Numbers and Strand Names ### 
    
    # Extract the rows where the first column value is 'Question difficulty', 'Strand', 'Precentage correct', and 'Question number'
    question_info = patData[patData.iloc[:, 0].isin(['Question difficulty', 'Strand', 'Percentage correct', 'Question number'])]
    
    # Reset the index of the extracted DataFrame
    question_info.reset_index(drop=True, inplace=True)

    # Remove all columns where question number is NaN
    question_info = question_info.dropna(axis=1, how='all')

    # Remove the last 2 columns
    question_info = question_info.iloc[:, :-2]

    # Rename the columns starting from the second column and starting from 1
    question_info.columns = ['QuestionNumber'] + [str(i) for i in range(1, question_info.shape[1])]
    
    # Drop 'Question number' row
    question_info = question_info[question_info['QuestionNumber'] != 'Question number']

    # Pivot the DataFrame to have 'Question Number' as index and the rest as columns
    question_info = question_info.set_index('QuestionNumber').T

    # Replace the values in the Strand column, N becomes 'Number', A becomes 'Algebra', Sp becomes 'Space', M becomes 'Measurement', St becomes 'Statistics' and P becomes 'Probability'
    question_info = question_info.replace({
        'N': 'Number',
        'A': 'Algebra',
        'Sp': 'Space',
        'M': 'Measurement',
        'St': 'Statistics',
        'P': 'Probability',
        'IE': 'Interpreting explicit information',
        'RI': 'Retrieving directly stated information',
        'RF': 'Reflecting on texts',
        'II': 'Interpreting by making inferences'
    })

    # Keep only the Index (QuestionNumber) and the Strand columns
    question_info = question_info[['Strand']]


    ### Extract Student Data ###

    # Find the index of the row where the first column is 'Unique ID'
    header_index = patData[patData.iloc[:, 0] == 'Unique ID'].index[0]

    # Slice all rows starting from the header row
    patData_responses = patData.iloc[header_index:].reset_index(drop=True)
    
    # Set the first row as header
    patData_responses.columns = patData_responses.iloc[0]
    
    # Remove the header row from the DataFrame data
    patData_responses = patData_responses.iloc[1:]

    # Remove columns, Family name, Given name, Middle name, Username, DOB, Gender, Year level (current), Active tags, Inactive tags, Tags (at time of test)
    patData_responses = patData_responses.drop(columns=['Family name', 'Given name', 'Middle names', 'Username', 'DOB', 'Gender', 'Year level (current)', 'Year level (at time of test)', 'Active tags', 'Inactive tags', 'Tags (at time of test)'])

    # Change the column names after Completed and before Score using their index positions
    columns_list = list(patData_responses.columns)
    completed_index = columns_list.index("Completed")
    score_index = columns_list.index("Score")

    # Loop through the columns between Completed and Score and set new names
    for i in range(completed_index + 1, score_index):
        columns_list[i] = str(i - completed_index)  # numeric names starting at 1 as string

    patData_responses.columns = columns_list

    # Define the columns to keep
    id_vars = ['Unique ID', 'Completed', 'Score', 'Scale', 'Stanine', 'Percentile']
    # All remaining columns will be pivoted; these become the "QuestionNumber" column
    value_vars = [col for col in patData_responses.columns if col not in id_vars]

    # Melt the DataFrame so that the question columns are consolidated
    patData_melted = pd.melt(patData_responses, 
                        id_vars=id_vars, 
                        value_vars=value_vars, 
                        var_name='QuestionNumber', 
                        value_name='Response')

    # Convert Response values: NA becomes blank, ✓ becomes True, and all other values become False
    patData_melted['Response'] = patData_melted['Response'].apply(
        lambda x: "" if pd.isna(x) else (True if x == '✓' else False)
    )

    # Add the test and test level to the melted DataFrame
    patData_melted['Test'] = test
    patData_melted['Test Level'] = test_level
    # Add the strand information to the melted DataFrame
    patData_melted = patData_melted.merge(question_info, left_on='QuestionNumber', right_index=True, how='left')
    # Reorder the columns
    patData_melted = patData_melted[['Unique ID', 'Test', 'Test Level', 'Completed', 'Score', 'Scale', 'Stanine', 'Percentile', 'QuestionNumber', 'Response'] + list(question_info.columns)]

    df = pd.concat([df, patData_melted], ignore_index=True)
    return df


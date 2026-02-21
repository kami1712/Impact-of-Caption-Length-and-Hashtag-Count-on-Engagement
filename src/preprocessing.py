# preprocessing.py
# Purpose: This script handles the initial data loading, filtering, adding derived columns like Caption_Length and Hashtags,
#          calculating Engagement Intention Score, renaming columns, merging files, and adding polynomial/interaction terms.
#          It prepares the core dataset for further analysis.
# Input Expectations: Requires 'data/original.xlsx' as input. Assumes columns like 'P101', 'P201', etc., exist.
# Output Delivery: Generates multiple CSV files in 'data/' folder, ending with 'merged_data_with_all_columns.csv'.
# Libraries Used:
# - pandas (pd): For data manipulation, reading/writing files, filtering, and calculations. Import: import pandas as pd
# Run this script first in the sequence.

import pandas as pd  # pandas library for data frames and CSV/Excel handling. Used to load, filter, and save data.

# Step 1: Load the original Excel file.
# Purpose: Read the input data into a DataFrame for processing.
input_file = 'data/original.xlsx'  # Input file path. Expect Excel with survey data.
df = pd.read_excel(input_file)  # Load Excel into pandas DataFrame. Handles sheets automatically if no sheet specified.

# Step 2: Calculate total rows in original file.
# Purpose: For logging and verification.
total_rows = len(df)  # Get number of rows using len() on DataFrame.
print(f"Total rows in original file: {total_rows}")  # Print for user feedback.

# Step 3: Filter for Instagram users (P101 == 1).
# Purpose: Keep only rows where participants use Instagram.
df_ig = df[df['P101'] == 1]  # Filter DataFrame using boolean mask. Keeps rows where condition is True.
ig_rows = len(df_ig)  # Recalculate rows after filter.
print(f"Rows after keeping P101==1: {ig_rows}")  # Corrected from original code's comment mismatch.

# Step 4: Save the filtered Instagram users data.
# Purpose: Output intermediate file for Instagram-only data.
df_ig.to_csv('data/IG_only.csv', index=False)  # Save to CSV without row indices.

# Step 5: Create main DataFrame for further splitting (same as df_ig).
df_main = df[df['P101'] == 1]  # Redundant but matches original code.

# Step 6: Create Q2.csv by removing specific columns.
# Purpose: Prepare subset for Question 2 analysis.
columns_to_remove_q2 = ['P301_CP', 'P301', 'P306', 'P302', 'P303', 'P304', 'P305']  # List of columns to drop.
df_q2 = df_main.drop(columns=columns_to_remove_q2, errors='ignore')  # Drop columns; ignore if missing.
df_q2.to_csv('data/Q2.csv', index=False)  # Save output.
print(f"Rows in Q2.csv: {len(df_q2)}")  # Log row count.

# Step 7: Create Q3.csv by removing specific columns.
# Purpose: Prepare subset for Question 3 analysis.
columns_to_remove_q3 = ['P201_CP', 'P201', 'P206', 'P202', 'P203', 'P204', 'P205']  # List of columns to drop.
df_q3 = df_main.drop(columns=columns_to_remove_q3, errors='ignore')  # Drop columns; ignore if missing.
df_q3.to_csv('data/Q3.csv', index=False)  # Save output.
print(f"Rows in Q3.csv: {len(df_q3)}")  # Log row count.

# Step 8: Filter Q2 for specific conditions (P206==3 and P202 in [3,4,5]).
# Purpose: Select interested respondents who identified Bochum correctly.
df_q2 = pd.read_csv('data/Q2.csv')  # Load previously saved Q2.csv.
rows_before_first_filter = len(df_q2)  # Log initial rows.
print(f"Rows in Q2.csv before filtering: {rows_before_first_filter}")
df_q2 = df_q2[df_q2['P206'] == 3]  # Filter for P206==3.
rows_after_first_filter = len(df_q2)  # Log after first filter.
print(f"Rows after selecting P206 == 3: {rows_after_first_filter}")
df_q2 = df_q2[df_q2['P202'].isin([3, 4, 5])]  # Further filter for P202 in list.
final_rows = len(df_q2)  # Log final rows.
print(f"Rows after selecting P202 in [3, 4, 5]: {final_rows}")
df_q2.to_csv('data/Cleaned_Q2.csv', index=False)  # Save cleaned output.
print("Cleaned_Q2.csv has been created successfully.")

# Step 9: Filter Q3 for specific conditions (P306==1 and P302 in [3,4,5]).
# Purpose: Select interested respondents who identified Climate Change correctly.
df_q3 = pd.read_csv('data/Q3.csv')  # Load Q3.csv.
rows_before = len(df_q3)  # Log initial rows.
print(f"Rows in Q3.csv before filtering: {rows_before}")
df_cleaned = df_q3[df_q3['P306'] == 1]  # Filter for P306==1.
print(f"Rows after filtering P306: {len(df_cleaned)}")  # Log.
df_cleaned = df_cleaned[df_cleaned['P302'].isin([3, 4, 5])]  # Filter for P302 in list.
rows_after = len(df_cleaned)  # Log final.
print(f"Rows after filtering (P306==1 and P302 in [3,4,5]): {rows_after}")
df_cleaned.to_csv('data/Cleaned_Q3.csv', index=False)  # Save.
print("Cleaned_Q3.csv has been created successfully.")

# Step 10: Define mapping for Caption_Length and Hashtags based on post code.
# Purpose: Coding scheme to derive new features from P201/P301.
coding_scheme = {  # Dictionary mapping post codes to (length, hashtags).
    1: (5, 5), 2: (70, 5), 3: (140, 5), 4: (200, 5),
    5: (5, 11), 6: (70, 11), 7: (140, 11), 8: (200, 11),
    9: (5, 15), 10: (70, 15), 11: (140, 15), 12: (200, 15)
}

# Step 11: Function to add Caption_Length and Hashtags to a DataFrame.
# Purpose: Reusable function to apply mapping and save enhanced file.
def add_post_info(df, post_col, output_file):  # Function takes DataFrame, column name, output path.
    df = df.copy()  # Copy to avoid modifying original.
    df['Caption_Length'] = pd.NA  # Initialize new column with NA (nullable).
    df['Hashtags'] = pd.NA  # Same for Hashtags.
    mask = df[post_col].isin(coding_scheme.keys())  # Mask for valid post values.
    valid_posts = df.loc[mask, post_col]  # Extract valid values.
    caption_lengths = valid_posts.map(lambda x: coding_scheme[x][0])  # Map to lengths using lambda.
    hashtags = valid_posts.map(lambda x: coding_scheme[x][1])  # Map to hashtags.
    df.loc[mask, 'Caption_Length'] = caption_lengths.values  # Assign back using loc to avoid warnings.
    df.loc[mask, 'Hashtags'] = hashtags.values  # Same.
    df['Caption_Length'] = df['Caption_Length'].astype('Int64')  # Convert to nullable int.
    df['Hashtags'] = df['Hashtags'].astype('Int64')  # Same.
    df.to_csv(f'data/{output_file}', index=False)  # Save to data folder.
    print(f"{output_file} created with {len(df)} rows.")  # Log.
    print(f" - Added: 'Caption_Length', 'Hashtags' based on '{post_col}'")  # Log.
    print(f" - Valid mappings: {mask.sum()} / {len(df)}\n")  # Log.
    return df  # Return enhanced DataFrame.

# Step 12: Apply to Q2.
print("Processing Cleaned_Q2.csv...")  # Log start.
df_q2 = pd.read_csv('data/Cleaned_Q2.csv')  # Load.
df_q2_enhanced = add_post_info(df_q2, 'P201', 'Cleaned_Q2_withPostInfo.csv')  # Call function.

# Step 13: Apply to Q3.
print("Processing Cleaned_Q3.csv...")  # Log.
df_q3 = pd.read_csv('data/Cleaned_Q3.csv')  # Load.
df_q3_enhanced = add_post_info(df_q3, 'P301', 'Cleaned_Q3_withPostInfo.csv')  # Call function.
print("Done! Both files enhanced successfully.")  # Log end.

# Step 14: Select and rename columns for Post1 (Q2).
# Purpose: Prepare final structure for Post1.
input_file = 'data/Cleaned_Q2_withPostInfo.csv'  # Input.
df = pd.read_csv(input_file)  # Load.
df_new = df[['SD01','SD02_01','SD10', 'P201', 'P202', 'P203', 'P204', 'P205','P206', 'Caption_Length', 'Hashtags']].copy()  # Select columns.
df_new = df_new.rename(columns={  # Rename for clarity.
    'SD01': 'Gender', 'SD02_01': 'Age', 'SD10': 'Occupation',
    'P201': 'Image Drawn', 'P206': 'Selection Criteria', 'P202': 'Post Interest',
    'P203': 'Like Possibility', 'P204': 'Comment Possibility', 'P205': 'Share Possibility'
})
df_new['Post'] = 1  # Add constant Post=1.
df_new['RowID'] = df_new.index.to_series().apply(lambda x: f"Post1_{x}")  # Create RowID.
df_new = df_new[['RowID','Gender','Age','Occupation', 'Post', 'Image Drawn', 'Post Interest', 'Like Possibility', 'Comment Possibility', 'Share Possibility', 'Caption_Length', 'Hashtags']]  # Reorder.
output_file = 'Cleaned_Q2_Final_Post1.csv'  # Output name.
df_new.to_csv(f'data/{output_file}', index=False)  # Save.
print(f"New file created successfully: {output_file}")  # Log.
print(f"Total rows: {len(df_new)}")  # Log.

# Step 15: Select and rename for Post2 (Q3).
input_file = 'data/Cleaned_Q3_withPostInfo.csv'  # Input.
df = pd.read_csv(input_file)  # Load.
df_new = df[['SD01','SD02_01','SD10', 'P301', 'P302', 'P303', 'P304', 'P305','P306', 'Caption_Length', 'Hashtags']].copy()  # Select.
df_new = df_new.rename(columns={  # Rename.
    'SD01': 'Gender', 'SD02_01': 'Age', 'SD10': 'Occupation',
    'P301': 'Image Drawn', 'P306': 'Selection Criteria', 'P302': 'Post Interest',
    'P303': 'Like Possibility', 'P304': 'Comment Possibility', 'P305': 'Share Possibility'
})
df_new['Post'] = 2  # Add Post=2.
df_new['RowID'] = df_new.index.to_series().apply(lambda x: f"Post2_{x}")  # RowID.
df_new = df_new[['RowID','Gender','Age','Occupation', 'Post', 'Image Drawn', 'Post Interest', 'Like Possibility', 'Comment Possibility', 'Share Possibility', 'Caption_Length', 'Hashtags']]  # Reorder.
output_file = 'Cleaned_Q3_Final_Post2.csv'  # Output.
df_new.to_csv(f'data/{output_file}', index=False)  # Save.
print(f"New file created successfully: {output_file}")  # Log.
print(f"Total rows: {len(df_new)}")  # Log.

# Step 16: Add Engagement Intention Score for Post1 (Q2) - inferred from similar Q3 code.
# Purpose: Calculate weighted score for engagement.
df_new = pd.read_csv('data/Cleaned_Q2_Final_Post1.csv')  # Load Post1.
df_new['Engagement Intention Score'] = (  # Weighted sum.
    df_new['Like Possibility'] * 0.847 +
    df_new['Comment Possibility'] * 0.941 +
    df_new['Share Possibility'] * 0.920
)
df_new['Engagement Intention Score'] = df_new['Engagement Intention Score'].round(2)  # Round to 2 decimals.
output_file = 'Cleaned_Q2_Post1_WithEngagementScore.csv'  # Output.
df_new.to_csv(f'data/{output_file}', index=False)  # Save.
print(f"Done! New file created: {output_file}")  # Log.
print(f"Total rows: {len(df_new)}")  # Log.

# Step 17: Add Engagement Intention Score for Post2 (Q3).
df_new = pd.read_csv('data/Cleaned_Q3_Final_Post2.csv')  # Load Post2.
df_new['Engagement Intention Score'] = (  # Same weights.
    df_new['Like Possibility'] * 0.847 +
    df_new['Comment Possibility'] * 0.941 +
    df_new['Share Possibility'] * 0.920
)
df_new['Engagement Intention Score'] = df_new['Engagement Intention Score'].round(2)  # Round.
output_file = 'Cleaned_Q3_Post2_WithEngagementScore.csv'  # Output.
df_new.to_csv(f'data/{output_file}', index=False)  # Save.
print(f"Done! New file created: {output_file}")  # Log.
print(f"Total rows: {len(df_new)}")  # Log.

# Step 18: Merge Post1 and Post2.
# Purpose: Combine into single dataset.
file1 = 'data/Cleaned_Q2_Post1_WithEngagementScore.csv'  # Input 1.
file2 = 'data/Cleaned_Q3_Post2_WithEngagementScore.csv'  # Input 2.
df1 = pd.read_csv(file1)  # Load.
df2 = pd.read_csv(file2)  # Load.
print("=== FILE INFO ===")  # Log.
print(f"{file1} → {len(df1):,} rows, {len(df1.columns)} columns")  # Log.
print(f"{file2} → {len(df2):,} rows, {len(df2.columns)} columns")  # Log.
if list(df1.columns) == list(df2.columns):  # Check columns match.
    print("Columns are IDENTICAL in both files")  # Log.
else:
    raise ValueError("Column mismatch! Fix before merging.")  # Error if not.
df_merged = pd.concat([df1, df2], ignore_index=True)  # Concat vertically.
df_merged['RowID'] = df_merged.index.to_series().apply(lambda x: f"Row_{x}")  # Reset RowID.
cols = ['RowID'] + [col for col in df_merged.columns if col != 'RowID']  # Move RowID first.
df_merged = df_merged[cols]  # Reorder.
print("\n=== MERGING SUCCESSFUL ===")  # Log.
print(f"Total rows in merged file : {len(df_merged):,}")  # Log.
output_file = 'merged_data.csv'  # Output.
df_merged.to_csv(f'data/{output_file}', index=False)  # Save.
print(f"\nMerged file saved as: {output_file}")  # Log.

# Step 19: Add polynomial and interaction terms.
# Purpose: Prepare for regression analysis.
df = pd.read_csv('data/merged_data.csv')  # Load merged.
print(f"Original data loaded: {len(df):,} rows, {len(df.columns)} columns")  # Log.
df['Hashtags^2'] = df['Hashtags'] ** 2  # Square Hashtags.
df['Caption_Length^2'] = df['Caption_Length'] ** 2  # Square Caption_Length.
df['Caption_Length_x_Hashtags'] = df['Caption_Length'] * df['Hashtags']  # Interaction.
df['(Caption_Length_x_Hashtags)^2'] = (df['Caption_Length'] * df['Hashtags']) ** 2  # Squared interaction.
print("\nNew columns added successfully!")  # Log.
print(f"Final data: {len(df):,} rows, {len(df.columns)} columns")  # Log.
output_file = 'merged_data_with_all_columns.csv'  # Final output.
df.to_csv(f'data/{output_file}', index=False)  # Save.
print(f"\nFile saved as: {output_file}")  # Log.

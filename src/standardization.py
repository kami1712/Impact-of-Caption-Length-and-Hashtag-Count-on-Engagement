# standardization.py
# Purpose: Standardizes numeric variables to z-scores, dummy-codes categoricals, and adds polynomial terms on z-scores for regression.
# Input Expectations: Requires 'data/merged_data_with_all_columns.csv' from preprocessing.
# Output Delivery: Saves 'data/FINAL_data_for_regression.csv'.
# Libraries Used:
# - pandas (pd): Data handling.
# - sklearn.preprocessing.StandardScaler: For z-scoring.
# Run after preprocessing.py.

import pandas as pd  # For data frames.
from sklearn.preprocessing import StandardScaler  # From scikit-learn, for standardization.

# Step 1: Load data.
# Purpose: Read merged file.
df = pd.read_csv('data/merged_data_with_all_columns.csv')  # Input path.

# Step 2: Define variables to standardize (numeric).
# Purpose: Select ordered/numeric columns for z-scoring.
to_standardize = [  # List of columns.
    'Age', 'Post Interest', 'Like Possibility',
    'Comment Possibility', 'Share Possibility',
    'Caption_Length', 'Hashtags',
    'Engagement Intention Score'
]

# Step 3: Define categorical variables for dummy-coding.
# Purpose: Select categoricals.
categorical = ['Gender', 'Occupation', 'Post', 'Image Drawn']  # List.

# Step 4: Standardize numeric variables.
# Purpose: Fit scaler and transform to z-scores.
scaler = StandardScaler()  # Initialize scaler (mean=0, std=1).
z_data = pd.DataFrame(  # Transform and create new DF with prefixed names.
    scaler.fit_transform(df[to_standardize]),
    columns=[f"z_{col}" for col in to_standardize]
)

# Step 5: Dummy-code categoricals.
# Purpose: Convert to binary dummies, drop first to avoid multicollinearity.
dummy_data = pd.get_dummies(df[categorical], drop_first=True, dtype=int)  # Get dummies.

# Step 6: Combine all.
# Purpose: Concat original (minus selected), z-data, dummies.
df_ready = pd.concat([  # Concat along columns.
    df.drop(columns=to_standardize + categorical).reset_index(drop=True),  # Drop originals.
    z_data,  # Add z-scores.
    dummy_data  # Add dummies.
], axis=1)

# Step 7: Add polynomial and interaction terms on z-scores.
# Purpose: For quadratic regression.
df_ready['z_Caption_Length_sq'] = df_ready['z_Caption_Length'] ** 2  # Square.
df_ready['z_Hashtags_sq'] = df_ready['z_Hashtags'] ** 2  # Square.
df_ready['z_Caption_x_Hashtags'] = df_ready['z_Caption_Length'] * df_ready['z_Hashtags']  # Interaction.
df_ready['z_Caption_x_Hashtags_sq'] = df_ready['z_Caption_x_Hashtags'] ** 2  # Squared interaction.

# Step 8: Save final file.
# Purpose: Output for regression.
df_ready.to_csv('data/FINAL_data_for_regression.csv', index=False)  # Save.
print("All done! Your new file is ready: FINAL_data_for_regression.csv")  # Log.
print(f"Columns: {list(df_ready.columns)}")  # Log columns.

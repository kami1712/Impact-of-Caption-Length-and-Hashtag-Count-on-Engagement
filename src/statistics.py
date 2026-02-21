# statistics.py
# Purpose: Computes descriptive statistics for thesis Section 4.4, like total cases, finished cases, randomization checks, completion time, missing answers.
# Input Expectations: Requires 'data/original.xlsx' with columns like 'FINISHED', 'P201', 'P301', 'TIME_SUM', 'MISSING'.
# Output Delivery: Prints statistics to console (copy-paste into thesis). No file outputs.
# Libraries Used:
# - pandas (pd): For data loading and calculations.
# Run after preprocessing.py (though independent).

import pandas as pd  # pandas for Excel reading and stats.

# Step 1: Load data, skipping sub-header row.
# Purpose: Read original Excel, skip row 1 (sub-header).
file_path = 'data/original.xlsx'  # Input path.
df = pd.read_excel(file_path, skiprows=[1])  # Load, skip row 1.

# Step 2: Compute total and finished cases.
# Purpose: Basic counts.
total_cases = len(df)  # Total rows.
finished_cases = len(df[df['FINISHED'] == 1])  # Filter and count finished.

# Step 3: Randomization checks for P201 and P301.
# Purpose: Verify unique codes and differences.
p201_codes = df['P201'].dropna().astype(int)  # Drop NaN, convert to int.
p301_codes = df['P301'].dropna().astype(int)  # Same.
all_codes_p201 = sorted(p201_codes.unique())  # Unique sorted list.
all_codes_p301 = sorted(p301_codes.unique())  # Same.
different_codes = (df['P201'] != df['P301']).sum()  # Count differences.
different_codes_pct = round(different_codes / finished_cases * 100, 1) if finished_cases > 0 else 0  # Percentage.

# Step 4: Completion time stats for finished cases.
# Purpose: Median and IQR time.
finished_df = df[df['FINISHED'] == 1].copy()  # Filter finished.
finished_df['TIME_SUM'] = pd.to_numeric(finished_df['TIME_SUM'], errors='coerce')  # Convert to numeric.
median_time = finished_df['TIME_SUM'].median()  # Median.
q25_time = finished_df['TIME_SUM'].quantile(0.25)  # 25th percentile.
q75_time = finished_df['TIME_SUM'].quantile(0.75)  # 75th.

# Step 5: Average missing answers percentage.
# Purpose: Mean of 'MISSING' column.
missing_percent_mean = df['MISSING'].astype(float).mean()  # Convert and mean.

# Step 6: Print all statistics.
# Purpose: Output for thesis.
print("=== FOR SECTION 4.4 ===")  # Header.
print(f"1. Total recorded cases : {total_cases}")  # Print 1.
print(f"2. Cases that reached final page : {finished_cases}")  # Print 2.
print(f"3. Codes in P201 (should be 1–12) : {all_codes_p201}")  # Print 3.
print(f" Codes in P301 (should be 1–12) : {all_codes_p301}")  # Print.
print(f"4. Participants with different codes : {different_codes} ({different_codes_pct} % of finished)")  # Print 4.
print(f"5. Median duration (seconds) : {median_time:.0f} (IQR {q25_time:.0f}–{q75_time:.0f})")  # Print 5.
print(f"6. Average % of missing answers : {missing_percent_mean:.2f}%")  # Print 6.

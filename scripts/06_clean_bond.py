# Pipeline-compatible copy: run using 11_run_pipeline.py.
#Loads the filtered tenancy bond dataset.
#Inspects its structure, data types, duplicates, missing values, and summary statistics.
#Replaces missing location identifiers (-99) with null values.
#Extracts the year and quarter from TimeFrame.
#Converts numeric columns to numeric types and categorical columns to category types.
#Saves the cleaned dataset to cleaned_tenancy_bonds_oct2025_jun2026.csv.

from pathlib import Path
import pandas as pd


# 2. Load processed Tenancy Bond dataset

tenancy_bond_data = pd.read_csv(
    pipeline_paths["bonds"]
)

# Store original dimensions
original_rows = len(tenancy_bond_data)
original_columns = len(tenancy_bond_data.columns)


# 3. Inspect dataset before cleaning

# Shape
print("\nDataset shape:")
print(tenancy_bond_data.shape)

# Column names
print("\nColumn names:")
print(tenancy_bond_data.columns.tolist())

# Data types
print("\nData types:")
print(tenancy_bond_data.dtypes)

# Missing values

# Convert the dataset's missing-location sentinel to a null value.
tenancy_bond_data["Location Id"] = tenancy_bond_data["Location Id"].replace(-99, pd.NA)

# Create year and quarter variables from TimeFrame
tenancy_bond_data["TimeFrame"] = pd.to_datetime(tenancy_bond_data["TimeFrame"])
tenancy_bond_data["year"] = tenancy_bond_data["TimeFrame"].dt.year
tenancy_bond_data["quarter"] = tenancy_bond_data["TimeFrame"].dt.month

# Convert the month number to the corresponding quarter
tenancy_bond_data["quarter"] = tenancy_bond_data["quarter"].replace({
    1: "JAN-MARCH",
    4: "APR-JUNE",
    7: "JULY-SEPT",
    10: "OCT-DEC"
})

print("\nColumn names:")
print(tenancy_bond_data.columns.tolist())


# number of duplicated rows
duplicate_rows = tenancy_bond_data.duplicated().sum()

print("\nDuplicate rows:")
print(f"Number of duplicate rows: {duplicate_rows}")

missing_count = tenancy_bond_data.isna().sum()
missing_percent = (missing_count / len(tenancy_bond_data) * 100).round(2)

missing_summary = pd.DataFrame({
    "missing_count": missing_count,
    "missing_percent": missing_percent
})

missing_summary = missing_summary[
    missing_summary["missing_count"] > 0
].sort_values("missing_percent", ascending=False)

print("\nMissing values:")
print(missing_summary)

# Summary statistics
print("\nNumeric summary statistics:")
print(tenancy_bond_data.describe().T)

print("\nText summary statistics:")
print(tenancy_bond_data.describe(include=["object"]).T)

#Setting number 

#numeric columns
numeric_columns = [
    "Total Bonds",
    "Active Bonds",
    "Closed Bonds",
    "Median Rent",
    "Geometric Mean Rent",
    "Upper Quartile Rent",
    "Lower Quartile Rent",
    "Log Std Dev Weekly Rent"
]

#categorical columns
categorical_columns = [
    "Location Id",
    "Dwelling Type",
    ]

print("\nNumeric columns:")
print(numeric_columns)  

print("\nCategorical columns:")
print(categorical_columns)


for column in numeric_columns:
    if column in tenancy_bond_data.columns:
        tenancy_bond_data[column] = pd.to_numeric(tenancy_bond_data[column], errors="coerce")

for column in categorical_columns:
    if column in tenancy_bond_data.columns:
        tenancy_bond_data[column] = tenancy_bond_data[column].astype("category")    


# Save the filtered dataset
tenancy_bond_data.to_csv(pipeline_paths["cleaned_bonds"],
    index=False)


from pathlib import Path
import pandas as pd


# 2. Load processed Christchurch dataset

df = pd.read_csv(
    "data/processed/tenancy_bonds_oct2025_jun2026.csv"
)

# Store original dimensions
original_rows = len(df)
original_columns = len(df.columns)


# 3. Inspect dataset before cleaning

# Shape
print("\nDataset shape:")
print(df.shape)

# Column names
print("\nColumn names:")
print(df.columns.tolist())

# Data types
print("\nData types:")
print(df.dtypes)

# Missing values

# Convert the dataset's missing-location sentinel to a null value.
df["Location Id"] = df["Location Id"].replace(-99, pd.NA)

#month year columns
df["TimeFrame"] = pd.to_datetime(df["TimeFrame"])  
df["year"] = df["TimeFrame"].dt.year
df["months"] = df["TimeFrame"].dt.month

#quarterly  
df["months"] = df["months"].replace({4: "JAN-MARCH", 7: "APR-JUNE", 10: "JULY-SEPT", 1: "OCT-DEC"})

df.loc[df["months"] == "OCT-DEC", "year"] = df["year"] -1 

print("\nColumn names:")
print(df.columns.tolist())


# number of duplicated rows
duplicate_rows = df.duplicated().sum()

print("\nDuplicate rows:")
print(f"Number of duplicate rows: {duplicate_rows}")

missing_count = df.isna().sum()
missing_percent = (missing_count / len(df) * 100).round(2)

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
print(df.describe().T)

print("\nText summary statistics:")
print(df.describe(include=["object"]).T)

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
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

for column in categorical_columns:
    if column in df.columns:
        df[column] = df[column].astype("category")    


# Save the filtered dataset
df.to_csv("data/processed/cleaned_tenancy_bonds_oct2025_jun2026.csv",
    index=False)

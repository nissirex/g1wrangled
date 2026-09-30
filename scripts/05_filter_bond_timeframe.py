#Loads the quarterly Tenancy Services dataset.
#Converts TimeFrame values to dates.
#Filters records from October 2025 through June 2026.
#Prints the included timeframes and row count.
#Saves the filtered data to tenancy_bonds_oct2025_jun2026.csv.

import pandas as pd


# Load the original Tenancy Services dataset
bond_data = pd.read_csv("data/raw/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv")


# Convert TimeFrame into a date
bond_data["TimeFrame"] = pd.to_datetime(bond_data["TimeFrame"])


# Keep the quarters that cover the same period as the
# Christchurch listings dataset: October 2025 to June 2026
bond_data = bond_data[
    (bond_data["TimeFrame"] >= "2025-10-01") &
    (bond_data["TimeFrame"] <= "2026-04-01")
]


# Show the results to check that the filtering worked
print("Timeframes included:")
print(bond_data["TimeFrame"].unique())

print("\nNumber of rows:")
print(len(bond_data))


# Save the filtered dataset
bond_data.to_csv("data/processed/tenancy_bonds_oct2025_jun2026.csv",
    index=False)
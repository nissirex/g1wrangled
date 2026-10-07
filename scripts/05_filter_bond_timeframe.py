# Pipeline-compatible copy: run using 11_run_pipeline.py.
# Loads the quarterly Tenancy Services dataset.
# Filters to quarters covering the selected Airbnb month range.

import pandas as pd
from pathlib import Path

# Load the original Tenancy Services dataset
bond_data = pd.read_csv(pipeline_paths["bond_source"])


# Convert TimeFrame into a date
bond_data["TimeFrame"] = pd.to_datetime(bond_data["TimeFrame"])


# Keep the quarters that cover the same period as the
# Christchurch listings dataset: October 2025 to June 2026
bond_data = bond_data[
    (bond_data["TimeFrame"] >= quarter_start) &
    (bond_data["TimeFrame"] <= quarter_end)
]


# Show the results to check that the filtering worked
print("Timeframes included:")
print(bond_data["TimeFrame"].unique())

print("\nNumber of rows:")
print(len(bond_data))


# Save the filtered dataset
bond_data.to_csv(pipeline_paths["bonds"],
    index=False)
print("Saved bond file:", Path(pipeline_paths["bonds"]).resolve())
print("File exists:", Path(pipeline_paths["bonds"]).is_file())

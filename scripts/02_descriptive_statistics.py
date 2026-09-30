# Describe the combined Christchurch listings before cleaning.
# Input: Combined listing CSV produced by script 01.
# Output: Numerical, categorical, identifier, date and missing-value summaries
# printed to the console. Run from the project root.

import pandas as pd

input_path = "data/processed/christchurch_listings_oct2025_jun2026.csv"

christchurch_data = pd.read_csv(input_path)

# Summaries describe listing observations across monthly snapshots.
# A listing can appear in more than one month.

# Numerical columns
numeric_columns = [
    "latitude",
    "longitude",
    "price",
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "calculated_host_listings_count",
    "availability_365",
    "number_of_reviews_ltm"
]
numeric_summary = christchurch_data[numeric_columns].describe().loc[["mean", "std", "min", "max"]]
print("Summary statistics for numerical columns:")
print(numeric_summary)


# Categorical columns
categorical_columns = [
    "name",
    "host_name",
    "neighbourhood_group",
    "neighbourhood",
    "room_type",
    "license"
]
categorical_summary = christchurch_data[categorical_columns].astype("string").describe().loc[["count", "unique", "top", "freq"]] #top returns the most common value
print("\nSummary statistics for categorical columns:")
print(categorical_summary)


# Identifier columns: distinguish observations from unique listings or hosts.
identifier_columns = ["id","host_id"]
identifier_summary = christchurch_data[identifier_columns].agg(["count", "nunique"]) #nunique counts the number of unique values
print("\nSummary statistics for identifier columns:")
print(identifier_summary)

# Parse dates for chronological summaries without changing the source columns.
date_columns = ["last_review","year_month"]
date_summary = christchurch_data[date_columns].astype("datetime64[ns]").describe().loc[["count", "min", "max"]]
print("\nSummary statistics for date columns:")
print(date_summary)

# Number of missing values per column
missing_values = christchurch_data.isnull().sum()
print("\nNumber of missing values per column:")
print(missing_values)

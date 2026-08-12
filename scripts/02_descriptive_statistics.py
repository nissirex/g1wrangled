import pandas as pd


df = pd.read_csv(
    "data/processed/christchurch_listings_oct2025_jun2026.csv"
)

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
numeric_summary = df[numeric_columns].describe().loc[["mean", "std", "min", "max"]]
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
categorical_summary = df[categorical_columns].astype("string").describe().loc[["count", "unique", "top", "freq"]] #top returns the most common value
print("\nSummary statistics for categorical columns:")
print(categorical_summary)


# Identifier columns
identifier_columns = ["id","host_id"]
identifier_summary = df[identifier_columns].agg(["count", "nunique"]) #nunique counts the number of unique values
print("\nSummary statistics for identifier columns:")
print(identifier_summary)

# Date columns
date_columns = ["last_review","year_month"]
date_summary = df[date_columns].astype("datetime64[ns]").describe().loc[["count", "min", "max"]]
print("\nSummary statistics for date columns:")
print(date_summary)

# Number of missing values per column
missing_values = df.isnull().sum()
print("\nNumber of missing values per column:")
print(missing_values)

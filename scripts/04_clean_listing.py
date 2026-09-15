# 1. Imports

from pathlib import Path
import pandas as pd


# 2. Load processed Christchurch dataset

df = pd.read_csv(
    "data/processed/christchurch_listings_oct2025_jun2026.csv"
)

print("Dataset loaded successfully.")

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

# 4. Remove unnecessary columns

columns_to_drop = [
    "name",
    "host_name",
    "license",
    "neighbourhood_group"
]

df = df.drop(columns=columns_to_drop)

print("\nColumns removed:")
print(columns_to_drop)

print("\nDataset shape after removing columns:")
print(df.shape)

# 5. Correct data types

# Numeric columns
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

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

# Date columns
date_columns = ["last_review"]

for column in date_columns:
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")

# Categorical columns
categorical_columns = [
    "neighbourhood",
    "room_type"
]

for column in categorical_columns:
    if column in df.columns:
        df[column] = df[column].astype("category")

print("\nData types after correction:")
print(df.dtypes)

# 6. Handle missing values

# Set reviews_per_month to 0 for listings with no reviews
if "reviews_per_month" in df.columns and "number_of_reviews" in df.columns:

    no_reviews = (
        df["reviews_per_month"].isna()
        & (df["number_of_reviews"] == 0)
    )

    reviews_filled = no_reviews.sum()
    df.loc[no_reviews, "reviews_per_month"] = 0

    print(
        "reviews_per_month values changed to 0:",
        reviews_filled
    )

# Keep last_review missing for listings that have never been reviewed

print("\nRemaining missing values:")
remaining_missing = df.isna().sum()
print(
    remaining_missing[
        remaining_missing > 0
    ].sort_values(ascending=False)
)

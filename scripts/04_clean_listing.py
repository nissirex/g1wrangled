# Clean the combined Christchurch listings: correct types, tidy text,
# remove unused columns and duplicate rows, and fill missing review rates
# only for listings with no reviews. Keep missing prices and minimum nights.
# Input: data/processed/christchurch_listings_oct2025_jun2026.csv.
# Output: data/processed/christchurch_listings_cleaned.csv and printed checks.
# Run from the project root. Raw data are not modified.

# Imports

from pathlib import Path
import pandas as pd
import numpy as np

output_path = Path("data/processed/christchurch_listings_cleaned.csv")

# Load processed Christchurch dataset

df = pd.read_csv(
    "data/processed/christchurch_listings_oct2025_jun2026.csv",
    dtype={"host_id": "string"}
)

print("Dataset loaded successfully.")

# Store original dimensions
original_rows = len(df)
original_columns = len(df.columns)

# Inspect dataset before cleaning

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

# Remove unnecessary columns

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

# Correct data types

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

# Nullable integers preserve missing values without rounding fractional values.
integer_columns = ["minimum_nights", "calculated_host_listings_count"]

for column in integer_columns:
    if column in df.columns:
        df[column] = df[column].astype("Int64")

# Date columns: snapshot/review dates are daily; year_month represents a month.
date_formats = {
    "last_review": "%Y-%m-%d",
    "Date": "%Y-%m-%d",
    "year_month": "%Y-%m",
}

for column, date_format in date_formats.items():
    if column in df.columns:
        original_dates = df[column]
        converted_dates = pd.to_datetime(
            original_dates,
            format=date_format,
            errors="coerce"
        )
        invalid_dates = (original_dates.notna() & converted_dates.isna()).sum()
        print(f"Invalid {column} values converted to missing: {invalid_dates}")
        df[column] = converted_dates

# Keep monthly precision and YYYY-MM values in the saved CSV.
if "year_month" in df.columns:
    df["year_month"] = df["year_month"].dt.to_period("M")

# Categorical columns (converted to strings during text cleaning below)
categorical_columns = [
    "neighbourhood",
    "room_type"
]

for column in categorical_columns:
    if column in df.columns:
        df[column] = df[column].astype("category")

print("\nData types after correction:")
print(df.dtypes)

# Handle missing values

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

# Clean text values

text_columns = df.select_dtypes(
    include=["object", "string", "category"]
).columns

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Replace blank or whitespace-only values with NaN

df = df.replace(r"^\s*$", np.nan, regex=True)

# Remove exact duplicates across the retained, standardised columns

rows_before_duplicates = len(df)

df = df.drop_duplicates()

duplicates_removed = rows_before_duplicates - len(df)

print("\nExact duplicate rows removed:")
print(duplicates_removed)

# Missing minimum_nights and price values are left missing.

# Check cleaned dataset

print("\nFinal missing values:")

final_missing = df.isna().sum()

print(
    final_missing[
        final_missing > 0
    ].sort_values(ascending=False)
)

print("\nDuplicate rows remaining:")
print(df.duplicated().sum())

print("\nFinal dataset shape:")
print(df.shape)

print("\nRows removed during cleaning:")
print(original_rows - len(df))

print("\nColumns removed during cleaning:")
print(original_columns - len(df.columns))

print("\nFinal data types:")
print(df.dtypes)

# Save cleaned dataset

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    output_path,
    index=False
)

print("\nCleaned dataset saved to:")
print(output_path)

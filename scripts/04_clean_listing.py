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

christchurch_data = pd.read_csv(
    "data/processed/christchurch_listings_oct2025_jun2026.csv",
    dtype={"host_id": "string"}
)


# Store original dimensions
original_rows = len(christchurch_data)
original_columns = len(christchurch_data.columns)

# Inspect dataset before cleaning

# Shape
print("\nDataset shape:")
print(christchurch_data.shape)

# Column names
print("\nColumn names:")
print(christchurch_data.columns.tolist())

# Data types
print("\nData types:")
print(christchurch_data.dtypes)

# Missing values
missing_count = christchurch_data.isna().sum()
missing_percent = (missing_count / len(christchurch_data) * 100).round(2)

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
print(christchurch_data.describe().T)

print("\nText summary statistics:")
print(christchurch_data.describe(include=["object"]).T)

# Remove unnecessary columns

columns_to_drop = [
    "name",
    "host_name",
    "license",
    "neighbourhood_group"
]

christchurch_data = christchurch_data.drop(columns=columns_to_drop)

print("\nColumns removed:")
print(columns_to_drop)

print("\nDataset shape after removing columns:")
print(christchurch_data.shape)

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
    if column in christchurch_data.columns:
        christchurch_data[column] = pd.to_numeric(christchurch_data[column], errors="coerce")

# Nullable integers preserve missing values without rounding fractional values.
integer_columns = ["minimum_nights", "calculated_host_listings_count"]

for column in integer_columns:
    if column in christchurch_data.columns:
        christchurch_data[column] = christchurch_data[column].astype("Int64")

# Date columns: snapshot/review dates are daily; year_month represents a month.
date_formats = {
    "last_review": "%Y-%m-%d",
    "Date": "%Y-%m-%d",
    "year_month": "%Y-%m",
}

for column, date_format in date_formats.items():
    if column in christchurch_data.columns:
        original_dates = christchurch_data[column]
        converted_dates = pd.to_datetime(
            original_dates,
            format=date_format,
            errors="coerce"
        )
        invalid_dates = (original_dates.notna() & converted_dates.isna()).sum()
        print(f"Invalid {column} values converted to missing: {invalid_dates}")
        christchurch_data[column] = converted_dates

# Keep monthly precision and YYYY-MM values in the saved CSV.
if "year_month" in christchurch_data.columns:
    christchurch_data["year_month"] = christchurch_data["year_month"].dt.to_period("M")

# Categorical columns (converted to strings during text cleaning below)
categorical_columns = [
    "neighbourhood",
    "room_type"
]

for column in categorical_columns:
    if column in christchurch_data.columns:
        christchurch_data[column] = christchurch_data[column].astype("category")

print("\nData types after correction:")
print(christchurch_data.dtypes)

# Handle missing values

# Set reviews_per_month to 0 for listings with no reviews
if "reviews_per_month" in christchurch_data.columns and "number_of_reviews" in christchurch_data.columns:

    no_reviews = (
        christchurch_data["reviews_per_month"].isna()
        & (christchurch_data["number_of_reviews"] == 0)
    )

    reviews_filled = no_reviews.sum()
    christchurch_data.loc[no_reviews, "reviews_per_month"] = 0

    print(
        "reviews_per_month values changed to 0:",
        reviews_filled
    )

# Keep last_review missing for listings that have never been reviewed

print("\nRemaining missing values:")
remaining_missing = christchurch_data.isna().sum()
print(
    remaining_missing[
        remaining_missing > 0
    ].sort_values(ascending=False)
)

# Clean text values

text_columns = christchurch_data.select_dtypes(
    include=["object", "string", "category"]
).columns

for column in text_columns:
    christchurch_data[column] = christchurch_data[column].astype("string").str.strip()

# Replace blank or whitespace-only values with NaN

christchurch_data = christchurch_data.replace(r"^\s*$", np.nan, regex=True)

# Remove exact duplicates across the retained, standardised columns

rows_before_duplicates = len(christchurch_data)

christchurch_data = christchurch_data.drop_duplicates()

duplicates_removed = rows_before_duplicates - len(christchurch_data)

print("\nExact duplicate rows removed:")
print(duplicates_removed)

# Missing minimum_nights and price values are left missing.

# Check cleaned dataset

print("\nFinal missing values:")

final_missing = christchurch_data.isna().sum()

print(
    final_missing[
        final_missing > 0
    ].sort_values(ascending=False)
)

print("\nDuplicate rows remaining:")
print(christchurch_data.duplicated().sum())

print("\nFinal dataset shape:")
print(christchurch_data.shape)

print("\nRows removed during cleaning:")
print(original_rows - len(christchurch_data))

print("\nColumns removed during cleaning:")
print(original_columns - len(christchurch_data.columns))

print("\nFinal data types:")
print(christchurch_data.dtypes)

# Save cleaned dataset

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

christchurch_data.to_csv(
    output_path,
    index=False
)

print("\nCleaned dataset saved to:")
print(output_path)

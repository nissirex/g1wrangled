# 1. Imports

from pathlib import Path
import pandas as pd
import numpy as np


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
date_columns = [
    "last_review",
    "Date"
]

for column in date_columns:
    if column in df.columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )
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

# 7. Clean text values

text_columns = df.select_dtypes(
    include=["object", "string", "category"]
).columns

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Replace blank or whitespace-only values with NaN

df = df.replace(r"^\s*$", np.nan, regex=True)

# 8. Remove exact duplicates

rows_before_duplicates = len(df)

df = df.drop_duplicates()

duplicates_removed = rows_before_duplicates - len(df)

print("\nExact duplicate rows removed:")
print(duplicates_removed)

# 9. Handle extreme prices

# Treat prices >= $5000 as missing so they can be imputed

extreme_price_count = (df["price"] >= 5000).sum()

df.loc[df["price"] >= 5000, "price"] = np.nan

print("\nPrices >= $5000 set to missing:")
print(extreme_price_count)

# 10. Minimum nights imputation

# First: median for the same month and room type
# Second: median for the same room type
# Third: overall median

minimum_nights_missing = df["minimum_nights"].isna().sum()

df["minimum_nights"] = (
    df.groupby(
        ["year_month", "room_type"],
        observed=True
    )["minimum_nights"]
    .transform(lambda x: x.fillna(x.median()))
    .fillna(
        df.groupby(
            "room_type",
            observed=True
        )["minimum_nights"].transform("median")
    )
    .fillna(df["minimum_nights"].median())
)

# Convert minimum_nights back to integer after imputation

df["minimum_nights"] = (
    df["minimum_nights"]
    .round()
    .astype("Int64")
)

print("\nMissing minimum_nights values imputed:")
print(minimum_nights_missing)

# 11. Price imputation

# First: median for neighbourhood + room type + minimum nights
# Second: median for room type
# Third: overall median

price_missing = df["price"].isna().sum()

df["price"] = (
    df.groupby(
        ["neighbourhood", "room_type", "minimum_nights"],
        observed=True
    )["price"]
    .transform(lambda x: x.fillna(x.median()))
    .fillna(
        df.groupby(
            "room_type",
            observed=True
        )["price"].transform("median")
    )
    .fillna(df["price"].median())
)

print("\nMissing/extreme price values imputed:")
print(price_missing)

# 12. Check cleaned dataset

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

# 13. Save cleaned dataset

output_path = Path(
    "data/processed/christchurch_listings_cleaned.csv"
)

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

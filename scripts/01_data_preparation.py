
import pandas as pd
import matplotlib.pyplot as plt

# Code used to filter and concatenate data

# List all of the datasets and their dates
files = [
("data/raw/listings_October2025.csv", "05/10/2025"),
("data/raw/listings_November2025.csv", "07/11/2025"),
("data/raw/listings_December2025.csv", "11/12/2025"),
("data/raw/listings_January2026.csv", "16/01/2026"),
("data/raw/listings_February2026.csv", "13/02/2026"),
("data/raw/listings_March2026.csv", "17/03/2026"),
("data/raw/listings_April2026.csv", "16/04/2026"),
("data/raw/listings_May2026.csv", "16/05/2026"),
("data/raw/listings_June2026.csv", "23/06/2026")
]

# Create an empty list to store the datasets
datasets = []

# Load and prepare each dataset
for file, date in files:

# Load the CSV file
df = pd.read_csv(file)

# Convert the date into a date
date = pd.to_datetime(date, format="%d/%m/%Y")

# Add the date to every row
df["Date"] = date

# Add a column containing just the month and year
df["year_month"] = date.strftime("%Y-%m")

# Keep only Christchurch City
df = df[df["neighbourhood_group"] == "Christchurch City"]

# Add the filtered dataset to our list
datasets.append(df)

# 4. Combine all nine Christchurch datasets
christchurch_data = pd.concat(datasets, ignore_index=True)

# 5. Save the combined dataset
christchurch_data.to_csv(
"data/processed/christchurch_listings_oct2025_jun2026.csv",
index=False
)

# 6. Print some basic information
print("Combined Christchurch dataset:")
print(christchurch_data)

print("\nNumber of rows:", len(christchurch_data))
print("Number of columns:", len(christchurch_data.columns))

print("\nColumns:")
print(christchurch_data.columns.tolist())
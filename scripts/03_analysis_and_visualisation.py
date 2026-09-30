# Explore review recency, prices and the most-reviewed Christchurch listings.
# Input: Combined listing CSV produced by script 01, before cleaning.
# Output: Printed summaries and two displayed histograms.
# Run from the project root.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

input_path = "data/processed/christchurch_listings_oct2025_jun2026.csv"
threshold = 1050
top_proportion = 0.10

christchurch_data = pd.read_csv(input_path)

# How long ago the last review was for each listing in the Christchurch dataset.

# Convert the date columns into dates
christchurch_data["Date"] = pd.to_datetime(
christchurch_data["Date"],
format="%Y-%m-%d"
)

christchurch_data["last_review"] = pd.to_datetime(
christchurch_data["last_review"]
)

# Calculate the number of days since the last review
christchurch_data["days_since_last_review"] = (
christchurch_data["Date"] -
christchurch_data["last_review"]
).dt.days

# Print summary statistics for the new variable
print("Summary statistics for days since last review:")
print(christchurch_data["days_since_last_review"].describe())

# Print days since the last review
print("\nDays since last review for each listing:")
print(christchurch_data["days_since_last_review"])

# Plot the distribution
print("\nPlotting the distribution of days since last review...")
plt.figure(figsize=(8,5))
plt.hist(
christchurch_data["days_since_last_review"].dropna(),
bins=30
)
plt.xlabel("Days since last review")
plt.ylabel("Number of listings")
plt.title("Distribution of Days Since Last Review")
plt.show()

# Price distribution across monthly listing observations
price = christchurch_data[['price']].copy()
clipped_data = np.clip(price, a_min=None, a_max=threshold)

# Missing values
missingValues = price.isna().sum()  # number of missing values 
#missing values
missingValues = price.isna().sum() 
print(f"Missing values in 'price' column: {missingValues}")

# Plotting histogram
plt.hist(clipped_data, bins=21, range=(0,threshold), edgecolor='black')
plt.title('Price Distribution')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Top 10% of Christchurch properties by number of reviews

christchurch_data["year_month"] = pd.to_datetime(
    christchurch_data["year_month"],
    format="%Y-%m"
)

# Sort each property chronologically
christchurch_data = christchurch_data.sort_values("year_month")

# Keep the latest record available for each property
latest_listings = christchurch_data.drop_duplicates(
    subset="id",
    keep="last"
)

# Sort by number of reviews
latest_listings = latest_listings.sort_values(
    by="number_of_reviews",
    ascending=False
)

# Keep top 10%
top_10_count = int(len(latest_listings) * 0.10)

top_10_percent = latest_listings.head(top_10_count)

print("Unique Christchurch properties:", len(latest_listings))
print("Properties in top 10%:", len(top_10_percent))

print(top_10_percent)


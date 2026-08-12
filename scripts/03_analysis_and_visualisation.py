import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np



# Load the Christchurch dataset
df = pd.read_csv(
"data/processed/christchurch_listings_oct2025_jun2026.csv"
)


# How long ago the last review was for each listing in the Christchurch dataset.

# Convert the date columns into dates
df["Date"] = pd.to_datetime(
df["Date"],
format="%Y-%m-%d"
)

df["last_review"] = pd.to_datetime(
df["last_review"]
)

# Calculate the number of days since the last review
df["days_since_last_review"] = (
df["Date"] -
df["last_review"]
).dt.days

# Print summary statistics for the new variable
print("Summary statistics for days since last review:")
print(df["days_since_last_review"].describe())

# Print days since the last review
print("\nDays since last review for each listing:")
print(df["days_since_last_review"])

# Plot the distribution
print("\nPlotting the distribution of days since last review...")
plt.figure(figsize=(8,5))

plt.hist(
df["days_since_last_review"].dropna(),
bins=30
)

plt.xlabel("Days since last review")
plt.ylabel("Number of listings")
plt.title("Distribution of Days Since Last Review")

plt.show()



price = df[['price']].copy()

# threshold for histogram
threshold = 1050

#1000+ prices all in this histogram col
clipped_data = np.clip(price, a_min=None, a_max=threshold)

#missing values
missingValues = price.isna().sum()  # number of missing values 
print(f"Missing values in 'price' column: {missingValues}")



#plotting histogram
plt.hist(clipped_data, bins=21, range=(0,threshold), edgecolor='black')
plt.title('Price Distribution')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Top 10% of Christchurch properties by number of reviews

df["year_month"] = pd.to_datetime(
    df["year_month"],
    format="%Y-%m"
)

# Sort each property chronologically
df = df.sort_values("year_month")

# Keep the latest record available for each property
latest_listings = df.drop_duplicates(
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


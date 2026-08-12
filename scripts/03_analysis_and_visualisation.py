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

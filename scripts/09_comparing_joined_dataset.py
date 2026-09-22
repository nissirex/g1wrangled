import pandas as pd
import matplotlib.pyplot as plt


# Load joined data
joined = pd.read_csv(
    "data/processed/joined_airbnb_tenancy.csv"
)


# Median Airbnb price in Christchurch Central
central = joined[
    pd.to_numeric(joined["sa2_code"], errors="coerce") == 326600
]

median_price = central["price"].median()

print(
    f"Median Airbnb price for Christchurch Central "
    f"(SA2 code 326600): ${median_price:,.2f}"
)


# Price gap between short- and long-term rentals
joined["long_term_price_per_night"] = (
    joined["Median Rent"] / 7
)

joined["price_difference"] = (
    joined["price"]
    - joined["long_term_price_per_night"]
)


# Median price gap for each location
price_gap = (
    joined
    .dropna(subset=["price_difference"])
    .groupby(["sa2_code", "sa2_name"])["price_difference"]
    .median()
    .reset_index()
    .sort_values("price_difference", ascending=False)
)

print("\nMedian price difference by location:")
print(price_gap.to_string(index=False))


largest_gap = price_gap.iloc[0]

print("\nLocation with largest median price gap:")
print("Location:", largest_gap["sa2_name"])
print("SA2 code:", largest_gap["sa2_code"])
print(
    f"Median difference: ${largest_gap['price_difference']:,.2f} per night"
)


# Plot distribution of price differences
plt.figure(figsize=(14, 7))

joined.boxplot(
    column="price_difference",
    by="sa2_name",
    rot=90
)

plt.title("Difference Between Short-Term and Long-Term Rental Prices")
plt.suptitle("")
plt.xlabel("Location")
plt.ylabel("Price difference per night ($)")
plt.tight_layout()

plt.savefig("price_difference_by_location.png", dpi=300)

plt.show()


# Number of Airbnbs in each location
airbnb_counts = (
    joined
    .groupby(["sa2_code", "sa2_name"])["id"]
    .nunique()
    .reset_index(name="airbnb_count")
    .sort_values("airbnb_count", ascending=False)
)

print("\nNumber of Airbnbs by location:")
print(airbnb_counts.to_string(index=False))


# Number of long-term rentals in each location
rental_data = (
    joined
    .dropna(subset=["Location Id"])
    .drop_duplicates(subset=["Location Id", "quarter"])
)

rental_counts = (
    rental_data
    .groupby("sa2_code")["Total Bonds"]
    .mean()
    .reset_index(name="average_rental_properties")
)

print("\nAverage number of long-term rentals by location:")
print(
    rental_counts
    .sort_values("average_rental_properties", ascending=False)
    .to_string(index=False)
)


# Compare Airbnb and long-term rentals
comparison = airbnb_counts.merge(
    rental_counts,
    on="sa2_code",
    how="outer"
)

comparison = comparison.sort_values(
    "airbnb_count",
    ascending=False
)

print("\nAirbnb vs long-term rentals by location:")
print(comparison.to_string(index=False))
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

# Keep observations with a price difference and ward name
plot_data = joined.dropna(
    subset=["price_difference", "neighbourhood"]
)

# Summarise price differences by ward
ward_summary = (
    plot_data.groupby("neighbourhood")
    .agg(
        median_gap=("price_difference", "median"),
        unique_airbnbs=("id", "nunique")
    )
    .sort_values("median_gap", ascending=False)
)

print(ward_summary)

fig, ax = plt.subplots(figsize=(12, 8))

plot_data.boxplot(
    column="price_difference",
    by="neighbourhood",
    vert=False,
    showfliers=False,
    ax=ax, grid=False
)

ax.set_title("Nightly price differences by Christchurch ward")
fig.suptitle("")
ax.set_xlabel("Airbnb price − weekly tenancy rent ÷ 7 (NZ$)")
ax.set_ylabel("Ward")

fig.tight_layout()
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
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("data/processed/christchurch_listings_cleaned_with_sa2.csv")

df["minimum_nights"] = pd.to_numeric(df["minimum_nights"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

#---median price for christchurch central------------------------------------------
median_price = df.loc[
    df["sa2_code"] == 326600,
    "price"
].median()

print(f"Median AirBnB price for Christchurch Central (SA2 code 326600): ${median_price:,.2f}")


#---price gap for short and long term per neighborhood-----------------------------

df = df.dropna(subset=["minimum_nights", "price", "sa2_name"])

df["stay_type"] = df["minimum_nights"].apply(
    lambda x: "short_term" if x <= 90 else "long_term"
)

long_term = df.loc[
    df["minimum_nights"] >= 91,
    ["sa2_name","minimum_nights", "price"]
].copy()

print(long_term)

print(df["stay_type"].value_counts())

# Compare average price by stay type within each neighborhood (SA2)
sa2_summary = (
    df.groupby(["sa2_name", "stay_type"], as_index=False)["price"]
      .mean()
      .pivot(index="sa2_name", columns="stay_type", values="price")
      .reset_index()
)

sa2_summary["price_gap"] = sa2_summary["short_term"] - sa2_summary["long_term"]

sa2_summary = sa2_summary[["sa2_name", "short_term", "long_term", "price_gap"]]

print(sa2_summary.sort_values("price_gap", ascending=False))
print("\n----------------------------------------------------------------------\n")

#---comparing how many rentals per location------------------------------------------------
totals_by_location = (
    df.groupby(["sa2_name"])
      .size()
      .reset_index(name="count")
      .sort_values("count", ascending=False)
)

print(totals_by_location)
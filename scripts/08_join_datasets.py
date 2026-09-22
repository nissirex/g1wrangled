import pandas as pd


# Load the datasets
airbnb = pd.read_csv("data/processed/christchurch_listings_cleaned_with_sa2.csv")

bonds = pd.read_csv("data/processed/cleaned_tenancy_bonds_oct2025_jun2026.csv")


# Create a quarter variable for the Airbnb data
airbnb["quarter"] = airbnb["year_month"].apply(
    lambda x:
        "OCT-DEC" if x in ["2025-10", "2025-11", "2025-12"]
        else "JAN-MARCH" if x in ["2026-01", "2026-02", "2026-03"]
        else "APR-JUNE"
)


# Tenancy Services

# Create the quarter variable from the TimeFrame
bonds["TimeFrame"] = pd.to_datetime(bonds["TimeFrame"])

bonds["quarter"] = bonds["TimeFrame"].dt.month.map({
    1: "JAN-MARCH",
    4: "APR-JUNE",
    7: "JULY-SEPT",
    10: "OCT-DEC"
})


# Check the quarters in both datasets
print("Airbnb quarters:")
print(airbnb["quarter"].value_counts())

print("\nTenancy quarters:")
print(bonds["quarter"].value_counts())


# Keep overall rental statistics
# "ALL" gives the overall value rather than a specific dwelling type or
# number of bedrooms
bonds_all = bonds[
    (bonds["Dwelling Type"] == "ALL") &
    (bonds["Number Of Beds"] == "ALL")
].copy()


# Remove rows without a Location ID because they cannot be joined
bonds_all = bonds_all.dropna(subset=["Location Id"])


# Check that each Location ID has only one record per quarter
duplicates = bonds_all.duplicated(
    subset=["Location Id", "quarter"]
).sum()

print("\nDuplicate location-quarter combinations:", duplicates)

# Convert SA2 codes and Location IDs to numeric for joining
airbnb["sa2_code"] = pd.to_numeric(
    airbnb["sa2_code"], errors="coerce"
).astype("Int64")

bonds_all["Location Id"] = pd.to_numeric(
    bonds_all["Location Id"], errors="coerce"
).astype("Int64")

# Join the datasets using SA2 area and quarter
# A left join keeps all Airbnb listings
joined = airbnb.merge(
    bonds_all,
    left_on=["sa2_code", "quarter"],
    right_on=["Location Id", "quarter"],
    how="left"
)


# Check that the join did not duplicate or remove Airbnb listings
print("\n========== JOIN CHECKS ==========")

print("Airbnb rows before join:", len(airbnb))
print("Rows after join:", len(joined))

if len(joined) == len(airbnb):
    print("Row count check: PASSED")
else:
    print("Row count check: WARNING - row count changed")


# Check how many Airbnb listings were matched
matched = joined["Location Id"].notna().sum()
unmatched = joined["Location Id"].isna().sum()

print("Airbnb listings matched to tenancy data:", matched)
print("Airbnb listings without matching tenancy data:", unmatched)


# Save the joined dataset
joined.to_csv("data/processed/joined_airbnb_tenancy.csv",
    index=False)

print("\nJoined dataset saved to:")
print("data/processed/joined_airbnb_tenancy.csv")
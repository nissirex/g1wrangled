import sqlite3
import pandas as pd


# 1. Load the two prepared datasets
airbnb = pd.read_csv(
    "data/processed/christchurch_listings_cleaned_with_sa2.csv"
)

bonds = pd.read_csv(
    "data/processed/cleaned_tenancy_bonds_oct2025_jun2026.csv"
)


# 2. Create matching year-quarter values, such as 2025Q4
airbnb["year_quarter"] = (
    pd.to_datetime(airbnb["year_month"])
    .dt.to_period("Q")
    .astype(str)
)

bonds["year_quarter"] = (
    pd.to_datetime(bonds["TimeFrame"])
    .dt.to_period("Q")
    .astype(str)
)


# 3. Open SQLite and store both datasets as tables
with sqlite3.connect("data/processed/christchurch_rentals.sqlite") as conn:

    airbnb.to_sql(
        "airbnb", conn, if_exists="replace", index=False
    )

    bonds.to_sql(
        "bonds", conn, if_exists="replace", index=False
    )

    # 4. Join by location and year-quarter using SQL
    query = """
        SELECT
            a.*,
            b."Location Id",
            b."Median Rent",
            b."Total Bonds",
            b."Active Bonds"
        FROM airbnb AS a
        LEFT JOIN bonds AS b
            ON a.sa2_code = b."Location Id"
            AND a.year_quarter = b.year_quarter
            AND b."Dwelling Type" = 'ALL'
            AND b."Number Of Beds" = 'ALL'
    """

    joined = pd.read_sql_query(query, conn)


# 5. Check the join
print("Airbnb rows before join:", len(airbnb))
print("Rows after join:", len(joined))

assert len(joined) == len(airbnb), "Join changed the number of rows!"

matched = joined["Location Id"].notna()

print("Matched observations:", matched.sum())
print("Unmatched observations:", (~matched).sum())

print(
    joined[[
        "id", "sa2_code", "Location Id", "year_quarter",
        "price", "Median Rent"
    ]].head(10)
)


# 6. Save the joined dataset
joined.to_csv(
    "data/processed/joined_airbnb_tenancy_sql.csv",
    index=False
)

print("\nDatabase saved: data/processed/christchurch_rentals.sqlite")
print("Joined CSV saved: data/processed/joined_airbnb_tenancy_sql.csv")
import sqlite3
import pandas as pd


AIRBNB_INPUT = "data/processed/christchurch_listings_cleaned_with_sa2.csv"
BONDS_INPUT = "data/processed/cleaned_tenancy_bonds_oct2025_jun2026.csv"
DATABASE_FILE = "data/processed/christchurch_rentals.sqlite"
OUTPUT_FILE = "data/processed/joined_airbnb_tenancy_sql.csv"


def main():
    """Join Airbnb and Tenancy Services data using SQLite."""

    airbnb = pd.read_csv(AIRBNB_INPUT)
    bonds = pd.read_csv(BONDS_INPUT)

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

    with sqlite3.connect(DATABASE_FILE) as conn:

        airbnb.to_sql(
            "airbnb", conn, if_exists="replace", index=False
        )

        bonds.to_sql(
            "bonds", conn, if_exists="replace", index=False
        )

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

    rows_before = len(airbnb)
    rows_after = len(joined)

    print("Airbnb rows before join:", rows_before)
    print("Rows after join:", rows_after)
    print("Rows changed:", rows_after - rows_before)

    assert rows_after == rows_before, (
        "Join changed the number of Airbnb rows."
    )

    matched = joined["Location Id"].notna()

    print("Matched observations:", matched.sum())
    print("Unmatched observations:", (~matched).sum())

    print(
        joined[[
            "id", "sa2_code", "Location Id", "year_quarter",
            "price", "Median Rent"
        ]].head(10)
    )

    joined.to_csv(OUTPUT_FILE, index=False)

    print("\nDatabase saved:", DATABASE_FILE)
    print("Joined CSV saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
import pandas as pd


AIRBNB_INPUT = "data/processed/christchurch_listings_cleaned_with_sa2.csv"
BONDS_INPUT = "data/processed/cleaned_tenancy_bonds_oct2025_jun2026.csv"
OUTPUT_FILE = "data/processed/joined_airbnb_tenancy.csv"


def create_airbnb_quarter(year_month):
    """Convert an Airbnb year-month value into a year-quarter value."""

    date = pd.to_datetime(year_month, format="%Y-%m", errors="coerce")
    return date.dt.to_period("Q").astype("string")


def create_bond_quarter(timeframe):
    """Convert a Tenancy Services timeframe into a year-quarter value."""

    date = pd.to_datetime(timeframe, errors="coerce")
    return date.dt.to_period("Q").astype("string")


def main():
    """Join Airbnb listings with Tenancy Services data by SA2 and quarter."""

    airbnb = pd.read_csv(AIRBNB_INPUT)
    bonds = pd.read_csv(BONDS_INPUT)

    assert "year_month" in airbnb.columns, "Airbnb data must contain year_month."
    assert "sa2_code" in airbnb.columns, "Airbnb data must contain sa2_code."
    assert "TimeFrame" in bonds.columns, "Bond data must contain TimeFrame."
    assert "Location Id" in bonds.columns, "Bond data must contain Location Id."

    # Create a quarter from the actual dates so new months can be added
    # without changing this code.
    airbnb["quarter"] = create_airbnb_quarter(
        airbnb["year_month"]
    )

    bonds["quarter"] = create_bond_quarter(
        bonds["TimeFrame"]
    )

    assert airbnb["quarter"].notna().all(), (
        "Every Airbnb observation must have a valid quarter.")
    assert bonds["quarter"].notna().all(), (
        "Every Tenancy Services observation must have a valid quarter.")

    # Keep the overall rental statistics rather than statistics for a
    # particular dwelling type or number of bedrooms.
    bonds_all = bonds[
        (bonds["Dwelling Type"] == "ALL") &
        (bonds["Number Of Beds"] == "ALL")
    ].copy()

    # Remove rows without a Location ID because they cannot be joined
    bonds_all = bonds_all.dropna(subset=["Location Id"])

    # Convert the join columns to the same numeric type.
    airbnb["sa2_code"] = pd.to_numeric(
        airbnb["sa2_code"],
        errors="coerce"
    ).astype("Int64")

    bonds_all["Location Id"] = pd.to_numeric(
        bonds_all["Location Id"],
        errors="coerce"
    ).astype("Int64")


    duplicates = bonds_all.duplicated(
        subset=["Location Id", "quarter"]
    ).sum()

    assert duplicates == 0, (
        "Each Location Id and quarter must have at most one "
        "Tenancy Services record."
    )

    # A left join keeps every Airbnb listing, including listings without
    # matching Tenancy Services data.
    joined = airbnb.merge(
        bonds_all,
        left_on=["sa2_code", "quarter"],
        right_on=["Location Id", "quarter"],
        how="left",
        validate="many_to_one"
    )

    # Check how many Airbnb listings were matched.
    matched = joined["Location Id"].notna().sum()
    unmatched = joined["Location Id"].isna().sum()


    print("========== JOIN CHECKS ==========")
    print("Airbnb rows before join:", len(airbnb))
    print("Rows after join:", len(joined))
    print("Airbnb listings matched to tenancy data:", matched)
    print("Airbnb listings without matching tenancy data:", unmatched)

    # Show the quarters used in the join.
    print("\nAirbnb quarters:")
    print(airbnb["quarter"].value_counts().sort_index())

    print("\nTenancy quarters:")
    print(bonds_all["quarter"].value_counts().sort_index())

    joined.to_csv(OUTPUT_FILE, index=False)

    print("\nJoined dataset saved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
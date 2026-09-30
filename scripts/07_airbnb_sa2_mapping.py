import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


# Settings

INPUT_FILE = "data/processed/christchurch_listings_cleaned.csv"
OUTPUT_FILE = "data/processed/christchurch_listings_cleaned_with_sa2.csv"

API_KEY = "4547baa841774dccb26c0234f1f4381b"
LAYER_ID = 98970

KOORDINATES_URL = "https://koordinates.com/services/query/v1/vector.json"




def get_sa2(latitude, longitude):
    """Return the SA2 code and name for a given latitude and longitude."""

    params = {
        "key": API_KEY,
        "layer": LAYER_ID,
        "x": longitude,
        "y": latitude,
        "max_results": 3,
        "radius": 10000,
        "geometry": "false",
        "with_field_names": "true"
    }

    try:
        response = requests.get(KOORDINATES_URL, params=params, timeout=30)
        response.raise_for_status()

        result = response.json()

        features = (
            result["vectorQuery"]["layers"][str(LAYER_ID)]["features"]
        )

        # Find the SA2 polygon containing the Airbnb
        for feature in features:

            if feature["distance"] == 0:

                properties = feature["properties"]

                return (
                    properties["SA22019_V1_00"],
                    properties["SA22019_V1_00_NAME"]
                )

    except Exception as e:
        print(f"Error for ({latitude}, {longitude}): {e}")

    return None, None



def main():
    """Map Airbnb listing coordinates to SA2 areas and save the results."""

    # Load cleaned Airbnb data
    df = pd.read_csv(INPUT_FILE)

    assert "latitude" in df.columns, "Input must contain latitude."
    assert "longitude" in df.columns, "Input must contain longitude."

    print(f"Loaded {len(df)} Airbnb listings.")

    coordinates = (
        df[["latitude", "longitude"]]
        .dropna()
        .drop_duplicates()
    )

    coordinate_list = list(
        coordinates.itertuples(index=False, name=None)
    )

    print(f"Querying {len(coordinate_list)} unique coordinates...")

    results = {}

    # Query multiple coordinates at the same time
    with ThreadPoolExecutor(max_workers=8) as executor:

        futures = {
            executor.submit(get_sa2, latitude, longitude):
            (latitude, longitude)
            for latitude, longitude in coordinate_list
        }

        total = len(futures)

        for count, future in enumerate(as_completed(futures), start=1):

            latitude, longitude = futures[future]

            sa2_code, sa2_name = future.result()

            results[(latitude, longitude)] = (
                sa2_code,
                sa2_name
            )

            if count % 100 == 0 or count == total:
                print(f"Completed {count}/{total}")

    # Add SA2 code and name to each Airbnb listing
    df["sa2_code"] = df.apply(
        lambda row: results.get(
            (row["latitude"], row["longitude"]),
            (None, None)
        )[0],
        axis=1
    )

    df["sa2_name"] = df.apply(
        lambda row: results.get(
            (row["latitude"], row["longitude"]),
            (None, None)
        )[1],
        axis=1
    )

    print()
    print("Matched:", df["sa2_code"].notna().sum())
    print("Not matched:", df["sa2_code"].isna().sum())

    print()
    print(
        df[
            ["latitude", "longitude", "sa2_code", "sa2_name"]
        ].head()
    )

    # Save updated dataset
    df.to_csv(OUTPUT_FILE, index=False)

    print()
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
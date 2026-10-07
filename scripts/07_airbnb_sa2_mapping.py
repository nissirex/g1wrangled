# Pipeline-compatible copy: run using 11_run_pipeline.py.
import pandas as pd
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


# Settings

INPUT_FILE = pipeline_paths["cleaned"]
OUTPUT_FILE = pipeline_paths["mapped"]

api_key = None

LAYER_ID = 98970

KOORDINATES_URL = "https://koordinates.com/services/query/v1/vector.json"




def get_sa2(latitude, longitude):
    """Return the SA2 code and name for a given latitude and longitude."""

    params = {
        "key": api_key,
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
        raise RuntimeError(f"SA2 request failed for ({latitude}, {longitude}); check the connection and API key.") from None

    return None, None



def main():
    """Map Airbnb listing coordinates to SA2 areas and save the results."""
    global api_key

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

    results = {}

    # Reuse saved coordinate lookups when a later month range is processed.
    cache_paths = [
        Path("data/processed/christchurch_listings_cleaned_with_sa2.csv"),
        *Path("data/processed").glob("*/christchurch_listings_with_sa2.csv"),
    ]
    for cache_path in cache_paths:
        if not cache_path.is_file() or cache_path.resolve() == Path(OUTPUT_FILE).resolve():
            continue
        cached = pd.read_csv(
            cache_path,
            usecols=["latitude", "longitude", "sa2_code", "sa2_name"],
        ).dropna(subset=["latitude", "longitude", "sa2_code", "sa2_name"])
        for row in cached.itertuples(index=False, name=None):
            latitude, longitude, sa2_code, sa2_name = row
            results.setdefault((latitude, longitude), (sa2_code, sa2_name))

    uncached_coordinates = [
        coordinate for coordinate in coordinate_list if coordinate not in results
    ]
    print(
        f"Reusing {len(coordinate_list) - len(uncached_coordinates)} saved "
        f"coordinate lookups; querying {len(uncached_coordinates)} new coordinates..."
    )

    # Query multiple coordinates at the same time
    if uncached_coordinates:
        try:
            with open("api_key.txt", "r", encoding="utf-8") as file:
                api_key = file.read().strip()
        except FileNotFoundError as error:
            raise SystemExit(
                "Missing api_key.txt; it is required to map new coordinates."
            ) from error

    with ThreadPoolExecutor(max_workers=8) as executor:

        futures = {
            executor.submit(get_sa2, latitude, longitude):
            (latitude, longitude)
            for latitude, longitude in uncached_coordinates
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

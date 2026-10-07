# Pipeline-compatible copy: run using 11_run_pipeline.py.
# Combine selected Airbnb snapshots for Christchurch City.
# Input: files and output_path supplied by the pipeline.

import pandas as pd

datasets = []

for file, date in files:
    df = pd.read_csv(file, dtype={"id": "string", "host_id": "string"})
    date = pd.to_datetime(date, format="%d/%m/%Y")

    df["Date"] = date
    df["year_month"] = date.strftime("%Y-%m")

    df = df[df["neighbourhood_group"] == "Christchurch City"]
    datasets.append(df)

christchurch_data = pd.concat(datasets, ignore_index=True)

christchurch_data.to_csv(output_path, index=False)

print("Combined Christchurch dataset:")
print(christchurch_data)

print("\nNumber of rows:", len(christchurch_data))
print("Number of columns:", len(christchurch_data.columns))

print("\nColumns:")
print(christchurch_data.columns.tolist())
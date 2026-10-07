"""Run the Christchurch Airbnb and tenancy analysis for a configured month range."""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import runpy

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.chdir(PROJECT_ROOT)


def resolve_path(value):
    """Resolve a configured path relative to the project root."""
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def parse_month(value, setting_name):
    """Parse a month in YYYY-MM format and return a monthly Period."""
    if not re.fullmatch(r"\d{4}-\d{2}", value):
        raise SystemExit(f"{setting_name} must use YYYY-MM format; received {value!r}.")
    try:
        return pd.Period(datetime.strptime(value, "%Y-%m"), freq="M")
    except ValueError as error:
        raise SystemExit(f"Invalid {setting_name}: {value!r}.") from error


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--config",
    default="config.json",
    help="Configuration file (default: config.json).",
)
parser.add_argument("--start-month", help="Override the configured start month (YYYY-MM).")
parser.add_argument("--end-month", help="Override the configured end month (YYYY-MM).")
args = parser.parse_args()

config_path = resolve_path(args.config)
if not config_path.is_file():
    raise SystemExit(f"Configuration file not found: {config_path}")

with config_path.open(encoding="utf-8") as handle:
    config = json.load(handle)

start = parse_month(
    args.start_month or config["start_month"], "start_month"
)
end = parse_month(
    args.end_month or config["end_month"], "end_month"
)
if start > end:
    raise SystemExit("The start month must be on or before the end month.")

raw_data_dir = resolve_path(config["raw_data_dir"])
processed_data_dir = resolve_path(config["processed_data_dir"])
bond_source = resolve_path(config["bond_data_file"])

# Filenames follow the existing convention: listings_July2026.csv.
months = {}
month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
for path in raw_data_dir.glob("listings_*.csv"):
    match = re.fullmatch(r"listings_([A-Za-z]+)(\d{4})", path.stem)
    if match and match[1].capitalize() in month_names:
        number = month_names.index(match[1].capitalize()) + 1
        month = pd.Period(f"{match[2]}-{number:02d}", freq="M")
        if month in months:
            raise SystemExit(f"Multiple input files found for {month}.")
        months[month] = path

selected = pd.period_range(start, end, freq="M")
missing = [str(month) for month in selected if month not in months]
if missing:
    raise SystemExit(
        "Missing input files for: " + ", ".join(missing)
        + f". Add listings_<Month><Year>.csv files to {raw_data_dir}."
    )
print("Processing months:", ", ".join(map(str, selected)))

# Snapshot dates are source capture dates, used for review-recency analysis.
snapshot_dates = dict(config.get("snapshot_dates", {}))
files = []
for month in selected:
    path = months[month]
    date = snapshot_dates.get(path.name)
    if not date:
        date = input(
            f"Snapshot date for {path.name} (DD/MM/YYYY, from source details): "
        ).strip()
    try:
        parsed = datetime.strptime(date, "%d/%m/%Y")
    except ValueError as error:
        raise SystemExit(
            f"Invalid snapshot date for {path.name}: {date!r}; use DD/MM/YYYY."
        ) from error
    if pd.Period(parsed, freq="M") != month:
        raise SystemExit(
            f"Snapshot date for {path.name} must fall in {month}; received {date}."
        )
    files.append((str(path), parsed.strftime("%d/%m/%Y")))

if not bond_source.is_file():
    raise SystemExit(f"Tenancy bond input not found: {bond_source}")

output_dir = processed_data_dir / f"{start}_to_{end}"
output_dir.mkdir(parents=True, exist_ok=True)
plots_dir = output_dir / "plots"
plots_dir.mkdir(exist_ok=True)

# Remove this run's old figures so unavailable comparisons cannot be stale.
for name in ["review_recency.png", "price_distribution.png", "price_gaps.png"]:
    (plots_dir / name).unlink(missing_ok=True)

pipeline_paths = {
    "combined": str(output_dir / "christchurch_listings.csv"),
    "cleaned": str(output_dir / "christchurch_listings_cleaned.csv"),
    "bond_source": str(bond_source),
    "bonds": str(output_dir / "tenancy_bonds.csv"),
    "cleaned_bonds": str(output_dir / "cleaned_tenancy_bonds.csv"),
    "mapped": str(output_dir / "christchurch_listings_with_sa2.csv"),
    "joined": str(output_dir / "joined_airbnb_tenancy.csv"),
    "sql_joined": str(output_dir / "joined_airbnb_tenancy_sql.csv"),
    "database": str(output_dir / "christchurch_rentals.sqlite"),
}


def save_plot(name):
    plt.gcf().suptitle(f"Analysis period: {start} to {end}")
    plt.savefig(plots_dir / name, bbox_inches="tight", dpi=150)
    plt.close()


quarter_start = str(start.asfreq("Q").start_time.date())
quarter_end = str(end.asfreq("Q").start_time.date())
scripts = [
    "01_data_preparation.py", "02_descriptive_statistics.py",
    "03_analysis_and_visualisation.py", "04_clean_listing.py",
    "05_filter_bond_timeframe.py", "06_clean_bond.py",
    "07_airbnb_sa2_mapping.py", "08_join_datasets.py",
    "09_comparing_joined_dataset.py", "10_sqlite_join.py",
]

for script in scripts:
    if not (PROJECT_ROOT / "scripts" / script).is_file():
        raise SystemExit(f"Missing scripts/{script}.")

for script in scripts:
    print(f"\nRunning {script}...", flush=True)
    try:
        runpy.run_path(
            str(PROJECT_ROOT / "scripts" / script),
            init_globals={
                "files": files,
                "output_path": pipeline_paths["combined"],
                "pipeline_paths": pipeline_paths,
                "quarter_start": quarter_start,
                "quarter_end": quarter_end,
                "save_plot": save_plot,
            },
            run_name="__main__",
        )
        if script == "01_data_preparation.py":
            combined = pd.read_csv(pipeline_paths["combined"])
            if combined.empty or set(combined["year_month"]) != set(map(str, selected)):
                raise ValueError(
                    "The combined data does not contain Christchurch rows "
                    "for every selected month."
                )
        if script == "05_filter_bond_timeframe.py":
            bonds = pd.read_csv(pipeline_paths["bonds"])
            available = set(pd.to_datetime(bonds["TimeFrame"]).dt.to_period("Q").astype(str))
            expected = set(str(month.asfreq("Q")) for month in selected)
            if expected - available:
                print("No bond data for quarters:", ", ".join(sorted(expected - available)))
                print("Airbnb rows will be retained without matching rents.")
    except Exception as error:
        raise SystemExit(f"Pipeline stopped at {script}: {error}") from error

print(f"\nPipeline completed. Results: {output_dir}")
print(f"Saved plots: {plots_dir}")

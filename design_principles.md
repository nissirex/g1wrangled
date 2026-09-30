# Pipeline Design Principles

AI used: GitHub Copilot (MAI-Code-1.1-Flash).

This document was drafted with GitHub Copilot to describe the project design principles for the pipeline.

## Purpose and Scope

This project processes Christchurch Airbnb listing data alongside New Zealand Tenancy Services rental-bond data. The pipeline is organised as a sequence of numbered Python scripts so that data is progressively prepared, checked, enriched, joined, and analysed. The main analysis period is October 2025 to June 2026.

## 1. Pipeline Inputs

### Airbnb listing data

The pipeline starts with nine monthly Inside Airbnb CSV files stored in `data/raw/`:

- `listings_October2025.csv`
- `listings_November2025.csv`
- `listings_December2025.csv`
- `listings_January2026.csv`
- `listings_February2026.csv`
- `listings_March2026.csv`
- `listings_April2026.csv`
- `listings_May2026.csv`
- `listings_June2026.csv`

Each file contains listing identifiers, location coordinates, neighbourhood information, room type, prices, review information, availability, and host-related fields. The preparation stage adds the observation date and month, then retains listings in Christchurch City.

### Tenancy Services data

The rental-market input is:

`data/raw/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv`

It contains quarterly rental-bond information, including location identifiers, dwelling type, number of beds, bond counts, and rent measures. The pipeline uses the records covering the same period as the Airbnb observations and later selects the overall `ALL` dwelling-type and `ALL` bedroom categories for joining.

### External geographic service

The SA2-mapping stage uses the Koordinates vector-query API and the Stats NZ SA2-2019 layer (`98970`). Latitude and longitude coordinates are matched to SA2 codes and names. This is an external dependency rather than a local input file, so the mapping stage requires network access and a valid API key.

### KNIME role

KNIME was used as a no-code way to set up and prototype the pipeline structure before the work was formalised into the numbered Python scripts. It was not a separate project scope or a second analysis stream; it served as the initial workflow-building tool for the same data-processing task.

## 2. Pipeline Outputs

The main persisted outputs are stored in `data/processed/`:

| Output | Purpose |
| --- | --- |
| `christchurch_listings_oct2025_jun2026.csv` | Combined monthly Airbnb data filtered to Christchurch City. |
| `christchurch_listings_cleaned.csv` | Cleaned Airbnb data with selected columns, corrected types, handled missing values, and duplicate checks. |
| `tenancy_bonds_oct2025_jun2026.csv` | Tenancy Services data filtered to the Airbnb study period. |
| `cleaned_tenancy_bonds_oct2025_jun2026.csv` | Tenancy data with cleaned location values and derived year/quarter fields. |
| `christchurch_listings_cleaned_with_sa2.csv` | Cleaned Airbnb data enriched with SA2 codes and names. |
| `joined_airbnb_tenancy.csv` | Airbnb and tenancy data joined by SA2 location and quarter. |
| `joined_airbnb_tenancy_sql.csv` | Equivalent joined output produced through SQLite SQL. |
| `christchurch_rentals.sqlite` | SQLite database containing the prepared Airbnb and tenancy tables. |

The analysis scripts also produce console summaries, descriptive statistics, and interactive Matplotlib plots. The current `outputs/figures/` directory is reserved for figures but does not contain saved plots in the present pipeline state.

## 3. Main Pipeline Steps

The scripts are numbered in the intended processing order.

1. **Prepare Airbnb data** - [scripts/01_data_preparation.py](scripts/01_data_preparation.py) loads the nine monthly files, adds date fields, filters to Christchurch City, concatenates the data, and writes the initial processed dataset.
2. **Explore descriptive statistics** - [scripts/02_descriptive_statistics.py](scripts/02_descriptive_statistics.py) summarises numeric, categorical, identifier, and date columns and reports missing values.
3. **Perform exploratory analysis** - [scripts/03_analysis_and_visualisation.py](scripts/03_analysis_and_visualisation.py) calculates review-age measures, examines price distributions, identifies highly reviewed listings, and displays plots.
4. **Clean Airbnb listings** - [scripts/04_clean_listing.py](scripts/04_clean_listing.py) removes unnecessary columns, converts data types, handles missing values, trims text, removes exact duplicates, treats extreme prices, imputes selected numeric values, and saves the cleaned Airbnb data.
5. **Filter tenancy data** - [scripts/05_filter_bond_timeframe.py](scripts/05_filter_bond_timeframe.py) selects tenancy quarters aligned with the Airbnb study period and writes the filtered tenancy dataset.
6. **Clean tenancy data** - [scripts/06_clean_bond.py](scripts/06_clean_bond.py) converts the location sentinel `-99` to missing, derives year and quarter fields, checks duplicates and missingness, converts numeric fields, and saves the cleaned tenancy data.
7. **Map Airbnb listings to SA2 areas** - [scripts/07_airbnb_sa2_mapping.py](scripts/07_airbnb_sa2_mapping.py) queries the external geographic service for unique coordinates, attaches SA2 codes and names, reports matches, and saves the enriched Airbnb data.
8. **Join the datasets ** - [scripts/08_join_datasets.py](scripts/08_join_datasets.py) creates comparable quarter fields, filters tenancy records to overall categories, checks location-quarter uniqueness, performs a left join, validates the row count, and saves the joined CSV.
9. **Compare short- and long-term rental measures** - [scripts/09_comparing_joined_dataset.py](scripts/09_comparing_joined_dataset.py) compares Airbnb prices with weekly tenancy rents, summarises price gaps, and compares Airbnb counts with active rental-bond counts by location.
10. **Repeat the join with SQLite** - [scripts/10_sqlite_join.py](scripts/10_sqlite_join.py) stores the prepared datasets in SQLite, joins them using SQL and year-quarter keys, checks that the join preserves Airbnb rows, and exports a second joined CSV.

## 4. Coding and Software Strategies

### Staged and reproducible processing

The numbered scripts represent separate stages with clear input and output files. Raw files are kept in `data/raw/`, while generated datasets are written to `data/processed/`. This makes intermediate results inspectable and allows later stages to be rerun without repeating every earlier operation.

### Appropriate tools for each task

Python is used as the main pipeline language. pandas handles CSV input, transformation, grouping, missing values, and joins. NumPy supports numeric cleaning and price handling. Matplotlib supports exploratory visualisation. SQLite provides a second, database-oriented implementation of the final join and offers a compact way to store the prepared tables.

### Explicit data-quality decisions

The scripts inspect shapes, column names, data types, missing values, summary statistics, and duplicates. Numeric and date fields are converted explicitly, invalid values are coerced to missing where appropriate, and missing-value treatment is based on the meaning of each field. For example, listings with no reviews can have `reviews_per_month` set to zero, while `last_review` remains missing because no review date exists.

### Defensive validation

The pipeline checks that location-quarter combinations are not duplicated before joining and checks that a left join does not change the number of Airbnb rows. The SQLite implementation uses an assertion for the same row-preservation requirement. These checks help detect accidental many-to-many joins and unexpected data loss.

### Consistent temporal and geographic keys

Monthly Airbnb observations are converted to quarter labels or year-quarter values so they can be compared with quarterly tenancy observations. Geographic matching uses SA2 identifiers, with the SA2 code and tenancy location identifier converted to compatible numeric types before joining.

### Efficient external lookups

The SA2-mapping stage queries each unique coordinate only once, stores the results in memory, and uses a thread pool for concurrent requests. The results are then mapped back to all listings sharing those coordinates. This reduces repeated API calls and shortens the mapping stage.

### Separation of analysis and storage concerns

Exploratory scripts print summaries and display plots, while preparation scripts save reusable datasets. The final join is implemented both with pandas and SQLite, providing a cross-check between two processing approaches.

## Reproducibility and Limitations

The scripts use project-relative paths and should be run from the repository root. The pipeline depends on the expected local raw files, installed Python packages, internet access for SA2 mapping, and a valid API key. The current SA2 script contains the API key directly in the source code; a stronger implementation would load it from an environment variable or other secret-management mechanism.

The workflow is currently a collection of scripts rather than a single orchestrated command with dependency tracking. Scripts therefore need to be run in order, and interactive plots are not automatically saved as reproducible figure files. The binary KNIME workflow in `workflow/nz_listings_pipline.knwf` is retained as a workflow artifact, but this document describes the Python implementation represented by the numbered scripts.

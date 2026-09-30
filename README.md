# DATA422 Group Project

This repository has been created for our DATA422 group project. It will be used to practise collaborative work using Git and GitHub and to store project files developed throughout the course.

## Team Members

- Rexstane Nissi Stanley
- Byron Hayes
- Avish Prakash
- Iliana Sarri

## Repository Contents

- `README.md` – overview of the project and repository
- `.gitignore` – files and folders that Git should not track
- `test1.py`, 'team_guidelines.md' – shared test file used to practise collaborative editing

## Dataset

### Data Sources

This project uses the `listings.csv` summary dataset provided by [Inside Airbnb](https://insideairbnb.com/get-the-data/).

- **Dataset:** Airbnb listings
- **Geographical coverage:** New Zealand
- **Dataset period:** June 2026
- **File name:** `listings.csv`
- **File format:** CSV
- **Source:** Inside Airbnb
- **Data dictionary:** Inside Airbnb Data Dictionary

Each row in the dataset represents one Airbnb listing captured at the time the data was collected. The dataset contains summary information about the listing, its host, geographical location, room type, price, minimum stay requirements, reviews, availability and licence details.

The original dataset is stored locally by each team member and is not uploaded to GitHub due to its size.

## Data Dictionary

| Column | Data type | Description |
|---|---|---|
| `id` | Integer | Airbnb's unique identifier for the listing. |
| `name` | Text | The name or title of the listing displayed on Airbnb. |
| `host_id` | Integer | Airbnb's unique identifier for the host or user responsible for the listing. |
| `host_name` | Text | The name of the host. This is usually the host's first name or names. |
| `neighbourhood_group` | Text | The broader neighbourhood or regional grouping assigned to the listing. It is calculated from the listing's latitude and longitude using publicly available geographical boundaries. This field may be empty where no neighbourhood group is available. |
| `neighbourhood` | Text | The neighbourhood assigned to the listing based on its latitude and longitude and publicly available geographical boundaries. |
| `latitude` | Numeric | The latitude coordinate of the listing using the World Geodetic System 1984 (`WGS84`). |
| `longitude` | Numeric | The longitude coordinate of the listing using the World Geodetic System 1984 (`WGS84`). |
| `room_type` | Text | The type of accommodation offered. Common categories include `Entire home/apt`, `Private room`, `Shared room` and `Hotel room`. |
| `price` | Numeric | The daily or nightly price of the listing in the local currency. For the New Zealand dataset, this represents New Zealand dollars. The dollar sign in the exported data may be a technical formatting feature. |
| `minimum_nights` | Integer | The minimum number of nights that a guest must book for the listing. The minimum-stay requirement may differ for particular dates in the listing's calendar. |
| `number_of_reviews` | Integer | The total number of reviews received by the listing. |
| `last_review` | Date | The date of the most recent review received by the listing. This may be missing where a listing has not received any reviews. |
| `reviews_per_month` | Numeric | The average number of reviews received per month over the lifetime of the listing. This may be missing for listings without reviews. |
| `calculated_host_listings_count` | Integer | The number of listings associated with the host in the current New Zealand data collection. |
| `availability_365` | Integer | The number of days during the next 365 days for which the listing is shown as available in the calendar. A day may be unavailable because it has been booked or because the host has blocked it. |
| `number_of_reviews_ltm` | Integer | The number of reviews received by the listing during the last 12 months. |
| `license` | Text | The licence, permit or registration number associated with the listing, where one is provided. This field may contain missing values. |

This project also uses the `Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv` summary dataset provided by [Tenancy Services](https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/).

- **Dataset:** Rental bond data
- **Geographical coverage:** New Zealand
- **Dataset period:** January 2020 to April 2026
- **File name:** `Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv`
- **File format:** CSV
- **Source:** Tenancy Services website
- **Data dictionary:** Tenancy Services Data Dictionary

Each row in the dataset represents one rental property captured at the time the data was collected. The dataset contains aggregated rental bond information about the Timeframe, Location Id, Dwelling Type, Number Of Beds, Total Bonds, Active Bonds, Closed Bonds, Median Rent, Geometric Mean Rent, Upper Quartile Rent, Lower Quartile Rent, and Log Std Dev Weekly Rent.

The original dataset is stored locally by each team member and is not uploaded to GitHub due to its size.

## Data Dictionary

| Column | Data type | Description |
|---|---|---|
| `Timeframe` | Date | The start date of the quarter that the data relate to. |
| `Location Id` | Integer | A numeric identifier for the geographical area. The dataset uses the SA2-2019 geographical boundaries defined by Statistics NZ. Note: The column also allows null values |
| `Dwelling Type` | Text | The type of dwelling represented by the data. ALL represents all dwelling types combined. |
| `Number Of Beds` | Integer/Text | The number of bedrooms in the dwelling. ALL is unknown due to lack of domain knowledge |
| `Total Bonds` | Integer | The total number of rental bonds recorded for the specified timeframe and combination of location, dwelling type, and number of beds. |
| `Active Bonds` | Integer | The number of rental bonds that were active for the specified timeframe and combination of location, dwelling type, and number of beds. |
| `Closed Bonds` | Integer | The number of rental bonds that were closed for the specified timeframe and combination of location, dwelling type, and number of beds. |
| `Median Rent` | Integer | The median weekly rent for the specified group of rental properties. Note: The column also allows null values. |
| `Geometric Mean Rent` | Integer | The geometric mean of weekly rent. This is used as an alternative measure to the median because rental prices tend to be clustered at round numbers. Note: The column also allows null values. |
| `Upper Quartile Rent` | Integer | The upper quartile of weekly rent, representing the 75th percentile of the rental distribution. Note: The column also allows null values. |
| `Lower Quartile Range` | Integer | The lower quartile of weekly rent, representing the 25th percentile of the rental distribution. Note: The column also allows null values. |
| `Log Std Dev Weekly Rent` | Decimal | The standard deviation of the logarithm of weekly rents, describing the spread of rental prices on the log scale. Note: The column also allows null values. |



### Data Limitations

The rental bond data are provisional because Tenancy Services is continuing to migrate information between its legacy and new bond management systems. As a result, recent data may be incomplete or revised, and some recent figures may not be directly comparable with earlier periods. Tenancy Services also applies privacy protection measures, including fixed random rounding and suppression of results where fewer than five bonds are recorded for a particular selection.



## Data Storage

The downloaded Airbnb data files and Quarterly Tenancy data files are stored inside the local `data` directory:

```text
data/
├── raw/
│   ├── Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv
│   ├── listings_October2025.csv
│   ├── listings_November2025.csv
│   ├── listings_December2025.csv
│   ├── listings_January2026.csv
│   ├── listings_February2026.csv
│   ├── listings_March2026.csv
│   ├── listings_April2026.csv
│   ├── listings_May2026.csv
│   └── listings_June2026.csv
└── processed/
```

## Scripts

The Python scripts are organised according to the main stages of the Christchurch Airbnb and Quarterly Tenancy Bond data preparation and analysis.

| Script | Description |
| --- | --- |
| `01_data_preparation.py` | Loads and combines the monthly Airbnb datasets, filters the data to Christchurch, and creates the processed Christchurch dataset covering October 2025 to June 2026. |
| `02_descriptive_statistics.py` | Generates descriptive statistics to explore the main characteristics of the processed Christchurch Airbnb dataset. |
| `03_analysis_and_visualisation.py` | Performs further analysis and creates visualisations of the Christchurch Airbnb data. |
| `04_clean_listing.py` | Cleans the processed Christchurch Airbnb dataset by removing unnecessary columns, correcting data types, handling missing values, checking data quality, and preparing the final dataset for later analysis. |
| `05_filter_bond_timeframe.py` | Filters the timeframe of the Quarterly Tenancy data to cover the same months as the Christchurch Airbnb data and creates the processed tenancy bonds dataset covering October 2025 to June 2026|
| `06_clean_bond.py` | Produces statistics for missingness and summaries. Cleans the data by correcting data types, making a new column for quarterly intervals.|
| `07_airbnb_sa2_mapping.py` | Takes the cleaned Airbnb dataset and matches the coordinates to SA2 labels for each listing.|
| `08_join_datasets.py` | Merges the cleaned Airbnb dataset with the cleaned tenancy bond dataset by SA2 location and quarter so that each Airbnb listing is matched to the corresponding rental-market data for that area and time period.|
| `09_comparing_joined_dataset.py` | Produces statistics for median Airbnbprice in christchurch central, price difference between short and long-term rentals, and comparing how many Airbnb and rental properties there are in each location.|
| `10_sqlite_join.py` | Stores both prepared datasets in SQLite, joins them using SQL by SA2 location and year-quarter, and exports the joined dataset. |

## Christchurch Airbnb Data Cleaning

The combined Christchurch dataset contained 28,795 rows and 20 columns before cleaning.

- **Column removal:** `name`, `host_name`, `license`, and `neighbourhood_group` were removed. `name` and `host_name` were not required for the planned analysis, `license` was entirely missing, and `neighbourhood_group` contained only one value (`Christchurch City`). This reduced the dataset from 20 to 16 columns without removing any rows.
- **Data types:** Numeric, date and categorical columns were converted to appropriate data types to support subsequent analysis. No rows were affected.
- **Missing prices:** 10,667 `price` values (37.04%) were retained as missing because these listings may still be useful when analysing property counts. They will be excluded only from analyses requiring price.
- **Review data:** 2,627 missing `reviews_per_month` values were set to 0 after confirming that the corresponding listings had no reviews. Missing `last_review` values were retained because listings without reviews have no valid review date.

## Tenancy bonds Data Cleaning

The tenancy bond dataset contained 27,212  rows and 12 columns before cleaning.

- **Column removal:** No columns were removed due to a lack of knowledge over the dataset and requirements further along for.
- **Column addition:** Added a new column for quarterly months for clarity and use later in joining
- **Data types:** Numeric, date and categorical columns were converted to appropriate data types to support subsequent analysis. No rows were affected. Number Of Beds remains as string due to "ALL" and "5+" being options. Without further domain knowledge it is hard to know what "ALL" means. 
- **Missing values and Observation Review:** location ID had both missing values and "-99". However these rows seem to be totals (however these totals did not match with the sections). these are not removed yet due to a lack of domain knowledge. There are 94 missing values for Geometric Mean Rent, Upper Quartile Rent, Lower Quartile Rent, Log Std Dev Weekly Rent. This missingness corresponds to the missing location ID's and therefore are also not removed yet. 890 obersevations were missing Number of beds, these have not been imputed due to lack of domain knowledge as "ALL" is also in the field.
- **Duplicates** There are no duplicates in the data.

## SA2 Mapping

A Koordinates account and API key were created to query the [Stats NZ SA2-2019 layer](https://datafinder.stats.govt.nz/layer/98970-statistical-area-2-2019-generalised/) (ID `98970`). The `07_airbnb_sa2_mapping.py` script queries unique Airbnb coordinates using eight concurrent workers and appends `sa2_code` and `sa2_name` to the cleaned Christchurch dataset. The result is saved as `christchurch_listings_cleaned_with_sa2.csv` to avoid repeating queries.

## SQLite Join

The `10_sqlite_join.py` script stores both prepared datasets in `christchurch_rentals.sqlite`. It creates `year_quarter` from Airbnb `year_month` and tenancy `TimeFrame`, then uses SQL to left join on location and year-quarter, selecting tenancy rows with `ALL` dwelling types and bedrooms. The join retains 28,795 observations: 24,551 matched and 4,244 unmatched. Results are exported to `joined_airbnb_tenancy_sql.csv`.
 

## Dataset Joining
The `08_join_datasets.py` script joins the cleaned Christchurch Airbnb listings dataset with the cleaned Tenancy Services rental bond dataset. First, the two datasets are loaded and a common quarter variable is created. The Airbnb data contains monthly observations from October 2025 to June 2026, so these months are grouped into the corresponding quarters. The Tenancy Services dataset already contains the same quarter information in the `months` column, which is copied to a new `quarter` column to make the datasets consistent. The Tenancy Services data is then filtered to observations where `Dwelling Type` and `Number Of Beds` are both `ALL`, providing an overall rental statistic for each area rather than statistics for a specific dwelling type or number of bedrooms. Rows without a `Location Id` are removed because they cannot be matched to an Airbnb SA2 area. Before joining, the script checks that there is only one Tenancy Services record for each `Location Id` and quarter, which prevents the join from duplicating Airbnb listings. The datasets are then joined using the Airbnb `sa2_code` & `quarter` and the Tenancy Services `Location Id` & `quarter`. A left join is used so that all Airbnb listings are retained, including listings for which there is no matching Tenancy Services record. Finally, the script checks that the number of Airbnb rows has not changed, reports how many listings were matched and unmatched, and saves the resulting joined dataset as `joined_airbnb_tenancy.csv` for use in the subsequent analyses.

24,551 of the 28,795 Airbnb listings were matched, while 4,244 were unmatched (remain in the dataset because a left join was used). The unmatched listings came from 46 SA2 areas. Additional checks found that 26 of the 46 unmatched SA2 codes do not occur anywhere in the cleaned Tenancy Services dataset. The remaining unmatched areas do occur somewhere in the Tenancy Services data, but apparently do not have the specific ALL dwelling type + ALL beds combination used for the join. Tenancy Services also states that its data can be suppressed when there are fewer than five bonds for a particular selection, so suppression or lack of an applicable overall rental record may contribute to some missing matches. Therefore, it would be inappropriate to assume that the geographic mapping is wrong simply because a listing has no rental match.

## Code Cleanup and Sanity Checks

- **01 — Data preparation:** Added a short description, improved formatting and removed an unused import. Retained the original filtering and combination steps.
- **02 — Descriptive statistics:** Clarified the input path and comments, improved formatting and made date conversion explicit. Checked date summaries using sample data.
- **03 — Analysis and visualisation:** Removed an unused import, clarified plot labels and moved settings to the top. Documented price capping for display and the top-10% selection rule.
- **04 — Listing cleaning:** Removed price and minimum-night imputation and extreme-price filtering. Corrected date and identifier types and used nullable integers for minimum nights and host listing counts. Sample-data checks confirmed missing values were preserved and dates were converted correctly.
- **05 — Bond timeframe filtering:** Removed redundant comments and print statements and clarified file paths and variable names.
- **06 — Bond cleaning:** Improved naming and formatting and removed unnecessary imputation code. Reviewed missing values, data types and duplicate counts.
- **07 — SA2 mapping:** Renamed the API URL variable for clarity and added checks for latitude and longitude columns. Reported matched and unmatched listings.
- **08 — pandas join:** Organised the workflow into functions and calculated year-quarter values from dates. Added required-column, quarter and duplicate-key checks, plus many-to-one merge validation. Checked row counts and investigated unmatched SA2 areas.
- **09 — Rental comparisons:** Removed unnecessary comments and print statements and used clearer names for datasets and calculated results.
- **10 — SQLite join:** Added named file paths and a main function. Checked row counts before and after joining and reported matched and unmatched observations.

Syntax checks were completed for the revised scripts 01–04. Sample-data checks were used where noted; these do not replace a full pipeline run.


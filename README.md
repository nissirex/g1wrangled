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
| `Months` | Quartly months |


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
## Christchurch Airbnb Data Cleaning

The combined Christchurch dataset contained 28,795 rows and 20 columns before cleaning.

- **Column removal:** `name`, `host_name`, `license`, and `neighbourhood_group` were removed. `name` and `host_name` were not required for the planned analysis, `license` was entirely missing, and `neighbourhood_group` contained only one value (`Christchurch City`). This reduced the dataset from 20 to 16 columns without removing any rows.
- **Data types:** Numeric, date and categorical columns were converted to appropriate data types to support subsequent analysis. No rows were affected.
- **Missing prices:** 10,667 `price` values (37.04%) were retained as missing because these listings may still be useful when analysing property counts. They will be excluded only from analyses requiring price.
- **Review data:** 2,627 missing `reviews_per_month` values were set to 0 after confirming that the corresponding listings had no reviews. Missing `last_review` values were retained because listings without reviews have no valid review date.

- ## Tenancy bonds Data Cleaning

The tenancy bond dataset contained 27,212  rows and 12 columns before cleaning.

- **Column removal:** No columns were removed due to a lack of knowledge over the dataset and requirements further along for.
- **Column addition:** Added a new column for quarterly months for clarity and use later
- **Data types:** Numeric, date and categorical columns were converted to appropriate data types to support subsequent analysis. No rows were affected. Number Of Beds remains as string due to "ALL" and "5+" being options. Without further domain knowledge it is hard to know what "ALL" means. 
- **Missing values and Observation Review:** location ID had both missing values and "-99". However these rows seem to be totals (however these totals did not match with the sections). these are not removed yet due to a lack of domain knowledge. There are 94 missing values for Geometric Mean Rent, Upper Quartile Rent, Lower Quartile Rent, Log Std Dev Weekly Rent. This missingness corresponds to the missing location ID's and therefore are also not removed yet. 890 obersevations were missing Number of beds, these have not been imputed due to lack of domain knowledge as "ALL" is also in the field.
- **Duplicates** There are no duplicates in the data.   
 


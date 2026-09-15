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

### Data Source

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

## Data Storage

The downloaded Airbnb data files are stored inside the local `data` directory:

data/
├── raw/
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

## Scripts

The Python scripts are organised according to the main stages of the Christchurch Airbnb data preparation and analysis.

| Script | Description |
| --- | --- |
| `01_data_preparation.py` | Loads and combines the monthly Airbnb datasets, filters the data to Christchurch, and creates the processed Christchurch dataset covering October 2025 to June 2026. |
| `02_descriptive_statistics.py` | Generates descriptive statistics to explore the main characteristics of the processed Christchurch Airbnb dataset. |
| `03_analysis_and_visualisation.py` | Performs further analysis and creates visualisations of the Christchurch Airbnb data. |
| `04_clean_listing.py` | Cleans the processed Christchurch Airbnb dataset by removing unnecessary columns, correcting data types, handling missing values, checking data quality, and preparing the final dataset for later analysis. |

## Christchurch Airbnb Data Cleaning

The combined Christchurch dataset contained 28,795 rows and 20 columns before cleaning.

- **Column removal:** `name`, `host_name`, `license`, and `neighbourhood_group` were removed. `name` and `host_name` were not required for the planned analysis, `license` was entirely missing, and `neighbourhood_group` contained only one value (`Christchurch City`). This reduced the dataset from 20 to 16 columns without removing any rows.
- **Data types:** Numeric, date and categorical columns were converted to appropriate data types to support subsequent analysis. No rows were affected.
- **Missing prices:** 10,667 `price` values (37.04%) were retained as missing because these listings may still be useful when analysing property counts. They will be excluded only from analyses requiring price.
- **Review data:** 2,627 missing `reviews_per_month` values were set to 0 after confirming that the corresponding listings had no reviews. Missing `last_review` values were retained because listings without reviews have no valid review date.

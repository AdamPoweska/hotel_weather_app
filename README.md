# hotel_weather_app
A PySpark ETL job that enriches weather observations with hotel data. Missing hotel coordinates are filled in via the Geoapify Geocoding API, and both datasets are joined on a 4-character Geohash.

## Pipeline
1. **Read** hotel data (CSV, gzip) and weather data (Parquet, partitioned by date)
2. **Fill missing coordinates**: hotels with missing `Latitude` / `Longitude` are geocoded with the [Geoapify Geocoding API](https://www.geoapify.com/geocoding-api)
3. **Generate a Geohash**: a 4-character Geohash from latitude and longitude (`pygeohash`) is added to both datasets
4. **Join**: left join of weather with hotels on the Geohash column
5. **Encrypt sensitive data**
6. **Store** the enriched data as Parquet, partitioned by `year/month/day`

## Project structure
hotel_weather_app/
├── src/hotel_weather/
│   ├── main.py             # orchestration of the ETL steps
│   ├── config.py           # paths, Spark settings, file patterns
│   ├── readers.py          # reading hotel and weather data
│   ├── geocoding.py        # GeoapifyClient (API calls only, no Spark code)
│   └── transformations.py  # DataFrame logic: coordinates, geohash, join
├── output/                 # enriched data (generated, not committed)
├── .env                    # secrets (not committed)
└── README.md

## Requirements
- Python 3.10+
- Java (JDK 11 or 17, depending on your PySpark version)
- Python packages: `pyspark`, `pygeohash`, `requests`, `python-dotenv`

pip install pyspark pygeohash requests python-dotenv


## Configuration
Create a `.env` file in the project root (it is listed in `.gitignore`):
GEOAPIFY_API_KEY=your_token_here
PII_ENCRYPTION_KEY=our_key_here

Data and output paths, Spark memory and file patterns are set in `src/hotel_weather/config.py`.

## How to run
From the `hotel_weather_app` directory:
python3 -m src.hotel_weather.main


## Output
Enriched data (all fields from both datasets) is written as Parquet to `output/enriched/`, partitioned by `year`, `month` and `day`:

output/enriched/
└── year=2017/
    └── month=8/
        └── day=29/
            └── part-*.parquet

The write uses `overwrite` mode with dynamic partition overwrite, so re-running the job does not create duplicates (idempotent).

## Notes
- The weather dataset is the left side of the join, so weather rows from cells without any hotel have `NULL` in the hotel columns. This is expected.
- Hotels that cannot be geocoded keep `NULL` coordinates and therefore have no Geohash.
- Spark is run in local mode; increase `SPARK_DRIVER_MEMORY` in `config.py` for larger runs.

## Data
The dataset is too large to be hosted on GitHub. A small sample will be available for download.
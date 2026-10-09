import os
from pathlib import Path
from dotenv import load_dotenv

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = Path(__file__).resolve().parents[4]

# API Key
load_dotenv(PROJECT_ROOT / ".env")
API_KEY = os.environ["GEOAPIFY_API_KEY"]

# Data paths
DATA_DIR = DATA_ROOT / "hotel_weather_data"
HOTELS_PATH = str(DATA_DIR / "hotels")
WEATHER_PATH = str(DATA_DIR / "weather")
OUTPUT_PATH = str(PROJECT_ROOT / "output" / "enriched")

# Spark
APP_NAME = "hotel_weather_app"
SPARK_MASTER = "local[1]"
SPARK_DRIVER_MEMORY = "2g"

# File extensions
HOTELS_EXT = "*.csv.gz"
WEATHER_EXT = "*.c000.snappy.parquet"

# URLs
GEOAPIFY_URL = "https://api.geoapify.com/v1/geocode/search"

# PII
PII_FIELDS = ["Name", "Address"]
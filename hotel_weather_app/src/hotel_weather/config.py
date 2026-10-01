from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[4]

# Data paths
DATA_DIR = PROJECT_ROOT / "hotel_weather_data"
HOTELS_PATH = str(DATA_DIR / "hotels")
WEATHER_PATH = str(DATA_DIR / "weather")

# Spark
APP_NAME = "hotel_weather_app"
SPARK_MASTER = "local[1]"
SPARK_DRIVER_MEMORY = "1g"

# File extensions
HOTELS_EXT = "*.csv.gz"
WEATHER_EXT = "*.c000.snappy.parquet"
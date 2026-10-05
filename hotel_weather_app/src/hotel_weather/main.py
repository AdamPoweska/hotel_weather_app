import os
from pathlib import Path
from dotenv import load_dotenv
from pyspark.sql import SparkSession

from src.hotel_weather.config import (
    PROJECT_ROOT,
    APP_NAME,
    SPARK_MASTER,
    SPARK_DRIVER_MEMORY,
    HOTELS_PATH,
    WEATHER_PATH,
    HOTELS_EXT,
    WEATHER_EXT,
)

from src.hotel_weather.schemas import hotel_schema, weather_schema
from src.hotel_weather.readers import data_read
from src.geo import geoapify

"""
from hotel_weather.readers import read_hotels, read_weather
from hotel_weather.transformations import join_hotel_weather
"""

def create_spark_session(name, cores_no, memory):
    """
    Creates spark session by given arguments.
    """
    return (
        SparkSession.builder
        .appName(name)
        .master(cores_no)
        .config("spark.driver.memory", memory)
        .getOrCreate()
    )

# def main():
#     PROJECT_ROOT = Path(__file__).resolve().parents[2]
#     env_path = PROJECT_ROOT / ".env"

#     print("PROJECT_ROOT:", PROJECT_ROOT)
#     print(".env path:", env_path)
#     print(".env exists:", env_path.exists())

#     load_dotenv(env_path)

#     print("API key exists:", "GEOAPIFY_API_KEY" in os.environ)
#     print("API key:", os.environ.get("GEOAPIFY_API_KEY"))

def main():
    load_dotenv(PROJECT_ROOT / ".env")
    API_KEY = os.environ["GEOAPIFY_API_KEY"]
    geo_client = geoapify.GeoapifyClient(api_key=API_KEY)
    coords = geo_client.geocode("Americana Resort Properties US Dillon 135 Main St")
    print(coords)
    # spark = create_spark_session(
    #     name=APP_NAME,
    #     cores_no=SPARK_MASTER,
    #     memory=SPARK_DRIVER_MEMORY
    # )

    # PROJECT_ROOT = Path(__file__).resolve().parents[2]
    # load_dotenv(PROJECT_ROOT / ".env")

    # API_KEY = os.environ["GEOAPIFY_API_KEY"]
    # geo_client = geoapify.GeoapifyClient(api_key=API_KEY)
    # coords = geo_client.geocode("Americana Resort Properties US Dillon 135 Main St")
    # print(coords)
    # hotels_df = data_read(spark, HOTELS_EXT, hotel_schema, HOTELS_PATH)
    # weather_df = data_read(spark, WEATHER_EXT, weather_schema, WEATHER_PATH)
    # hotels_df.show(100, truncate=False)
    # weather_df.show(100, truncate=False)

    # try:
    #     hotels_df = data_read(spark, HOTELS_EXT, hotel_schema, HOTELS_PATH)
    #     weather_df = data_read(spark, WEATHER_PATH, weather_schema, WEATHER_EXT)

        # result_df = join_hotel_weather(
        #     hotels_df,
        #     weather_df
        # )

    #     result_df.show()

    # finally:
    #     spark.stop()


if __name__ == "__main__":
    main()

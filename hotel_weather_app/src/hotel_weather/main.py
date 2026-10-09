import pygeohash as pgh
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col
from pyspark.sql.types import StringType

from src.hotel_weather.config import (
    PROJECT_ROOT,
    APP_NAME,
    SPARK_MASTER,
    SPARK_DRIVER_MEMORY,
    HOTELS_PATH,
    WEATHER_PATH,
    HOTELS_EXT,
    WEATHER_EXT,
    GEOAPIFY_URL,
    API_KEY,
    OUTPUT_PATH,
    PII_FIELDS,
)

from src.hotel_weather.schemas import hotel_schema, weather_schema
from src.hotel_weather.readers import data_read
from src.geo import geoapify
from src.hotel_weather.transformations.transformations import fill_missing_coordinates, add_geohash, join_weather_hotels
from src.hotel_weather.encryption import PIIEncryptor

"""
from hotel_weather.readers import read_hotels, read_weather
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

@F.udf(returnType=StringType())
def geohash4(lat, lon):
    if lat is None or lon is None:
        return None
    return pgh.encode(lat, lon, precision=4)


def main():
    # spark creation
    spark = create_spark_session(
        name=APP_NAME,
        cores_no=SPARK_MASTER,
        memory=SPARK_DRIVER_MEMORY
    )

    # client geoapify
    geo_client = geoapify.GeoapifyClient(api_key=API_KEY, url=GEOAPIFY_URL)

    # dataframe creation
    hotels_df = data_read(spark, HOTELS_EXT, hotel_schema, HOTELS_PATH, "csv")
    weather_df = data_read(spark, WEATHER_EXT, None, WEATHER_PATH, "parquet") # for parquet schema is in the file, no need to pass it

    # adding missing coordiantes - geoapify
    hotels_df = fill_missing_coordinates(spark, hotels_df, geo_client)

    # adding geohash
    hotels_df = add_geohash(hotels_df, "Latitude", "Longitude")
    weather_df = add_geohash(weather_df, "lat", "lng")

    # idempotency
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    # enriching data
    enriched_df = join_weather_hotels(weather_df, hotels_df)
    enriched_df = PIIEncryptor().encrypt(enriched_df, PII_FIELDS)

    # write
    (
        enriched_df
        .repartition("year", "month", "day")
        .write
        .mode("overwrite")
        .partitionBy("year", "month", "day")
        .parquet(OUTPUT_PATH)
    )


if __name__ == "__main__":
    main()

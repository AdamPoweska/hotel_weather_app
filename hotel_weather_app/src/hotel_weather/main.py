import pygeohash as pgh
# from pathlib import Path
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
)

from src.hotel_weather.schemas import hotel_schema, weather_schema
from src.hotel_weather.readers import data_read
from src.geo import geoapify
from src.hotel_weather.transformations.hotel_transformations import fill_missing_coordinates, add_geohash

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
    """
    geo_client = geoapify.GeoapifyClient(api_key=API_KEY, url=GEOAPIFY_URL)
    coords = geo_client.geocode("Americana Resort Properties US Dillon 135 Main St")
    print(coords)
    
    coords = (-33.481565, 150.156498)
    print(coords[0])
    geohash = pgh.encode(coords[0], coords[1])
    print(geohash)
    lat, lng = pgh.decode(geohash=geohash)
    print(lat, lng)
    """
    # tworzymy sparka
    spark = create_spark_session(
        name=APP_NAME,
        cores_no=SPARK_MASTER,
        memory=SPARK_DRIVER_MEMORY
    )

    # client geoapify
    geo_client = geoapify.GeoapifyClient(api_key=API_KEY, url=GEOAPIFY_URL)

    # Zaczytanie danych do df
    hotels_df = data_read(spark, HOTELS_EXT, hotel_schema, HOTELS_PATH, "csv")
    weather_df = data_read(spark, WEATHER_EXT, None, WEATHER_PATH, "parquet") # for parquet schema is in the file, no need to pass it

    # uzupełnenie danych
    hotels_df = fill_missing_coordinates(spark, hotels_df, geo_client)
    hotels_df = add_geohash(hotels_df, "Latitude", "Longitude")
    weather_df = add_geohash(weather_df, "lat", "lng")

    # stare:
    # hotels_df = hotels_df.withColumn("Latitude", col("Latitude").cast("double"))
    # hotels_df = hotels_df.withColumn("Longitude", col("Longitude").cast("double"))

    # weather df
    


    # hotels_df = hotels_df.withColumn("geohash", geohash4("Latitude", "Longitude"))
    # weather_df = weather_df.withColumn("geohash", geohash4("lat", "lng"))

    # hotels_df.show(100, truncate=False)
    # weather_df.show(100, truncate=False)

    hotels_df.select("Name", "Latitude", "Longitude", "geohash").show(10, truncate=False)
    weather_df.show(100, truncate=False)
    
    for name, df in [("hotels", hotels_df), ("weather", weather_df)]:
        print(name, "wierszy:", df.count(), 
            "| bez geohasha:", df.filter(F.col("geohash").isNull()).count())
    df.select("geohash").distinct().show(5)

    hotels_df.select("geohash").filter(F.length("geohash") != 4).count()  # powinno być 0
    
    weather_df.printSchema()
    weather_df.show(5, truncate=False)
    # hotels_df.filter(F.col("geohash").isNull()).count().show(10)   # ile hoteli bez hasha
    # weather_df.show(100, truncate=False)

    # coords = geo_client.geocode("Americana Resort Properties US Dillon 135 Main St")
    # print(coords)
    
    # coords = (-33.481565, 150.156498)
    # print(coords[0])
    # geohash = pgh.encode(coords[0], coords[1])
    # print(geohash)
    # lat, lng = pgh.decode(geohash=geohash)
    # print(lat, lng)

    # hotels_df = data_read(spark, HOTELS_EXT, hotel_schema, HOTELS_PATH)
    # weather_df = data_read(spark, WEATHER_EXT, weather_schema, WEATHER_PATH)
    # hotels_df.show(100, truncate=False)
    # weather_df.show(100, truncate=False)

    # try:
    #     hotels_df = data_read(spark, HOTELS_EXT, hotel_schema, HOTELS_PATH)
    #     weather_df = data_read(spark, WEATHER_PATH, weather_schema, WEATHER_EXT)

    #     result_df = join_hotel_weather(
    #         hotels_df,
    #         weather_df
    #     )

    #     result_df.show()

    # finally:
    #     spark.stop()


if __name__ == "__main__":
    main()

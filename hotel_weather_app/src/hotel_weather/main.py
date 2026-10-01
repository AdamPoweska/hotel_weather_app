from pyspark.sql import SparkSession

from config import (
    APP_NAME,
    SPARK_MASTER,
    SPARK_DRIVER_MEMORY,
    HOTELS_PATH,
    WEATHER_PATH,
    HOTELS_EXT,
    WEATHER_EXT,
)

from schemas import hotel_schema, weather_schema
from readers import data_read

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


def main():
    spark = create_spark_session(
        name=APP_NAME,
        cores_no=SPARK_MASTER,
        memory=SPARK_DRIVER_MEMORY
    )

    hotels_df = data_read(spark, HOTELS_EXT, hotel_schema, HOTELS_PATH)
    weather_df = data_read(spark, WEATHER_EXT, weather_schema, WEATHER_PATH)
    hotels_df.show(100, truncate=False)
    weather_df.show(100, truncate=False)

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

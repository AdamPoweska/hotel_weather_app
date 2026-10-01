from pyspark.sql import SparkSession

from config import (
    APP_NAME,
    SPARK_MASTER,
    SPARK_DRIVER_MEMORY,
    HOTELS_PATH,
    WEATHER_PATH,
)

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

    # try:
    #     hotels_df = read_hotels(spark, HOTELS_PATH)
    #     weather_df = read_weather(spark, WEATHER_PATH)

    #     result_df = join_hotel_weather(
    #         hotels_df,
    #         weather_df
    #     )

    #     result_df.show()

    # finally:
    #     spark.stop()


if __name__ == "__main__":
    main()

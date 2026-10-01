#TODO: python code here

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

spark = (
    SparkSession.builder
    .appName("hotel_weather_app")
    .master("local[1]") # 1 core used locally
    .config("spark.driver.memory", "512m") # m = MB, g = GB
    .getOrCreate()
)

hotel_schema = StructType([
    StructField("Id", StringType(), True), # par: name, dataType, nullable, metadata-optional-dict
    StructField("Name", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("City", StringType(), True),
    StructField("Address", StringType(), True),
    StructField("Latitude", StringType(), True),
    StructField("Longitude", StringType(), True)
])

weather_schema = StructType([
    StructField("lng", DoubleType(), True),
    StructField("lat", DoubleType(), True),
    StructField("avg_tmpr_f", DoubleType(), True),
    StructField("avg_tmpr_c", DoubleType(), True),
    StructField("wthr_date", StringType(), True),
    StructField("wthr_year", StringType(), True),
    StructField("wthr_month", StringType(), True),
    StructField("wthr_day", StringType(), True)
])

BASE_PATH_HOTEL = "../../../../../m06sparkbasics/m06sparkbasics/hotels"
BASE_PATH_WEATHER = "../../../../../m06sparkbasics/m06sparkbasics/weather"

hotel_df = (
    spark.read
    .option("header", True)
    .option("recursiveFileLookup", True)
    .option("pathGlobFilter", "*.csv.gz")
    .schema(hotel_schema)
    .csv(BASE_PATH_HOTEL)
)

weather_df = (
    spark.read
    .option("header", True)
    .option("recursiveFileLookup", True)
    .option("pathGlobFilter", "*.c000.snappy.parquet")
    .schema(weather_schema)
    .csv(BASE_PATH_WEATHER)
)

hotel_df.printSchema()
weather_df.printSchema()

hotel_df.show(100, truncate=False)
weather_df.show(100, truncate=False)

print("Liczba partycji - hotel_df:", hotel_df.rdd.getNumPartitions())
print("Liczba partycji - weather_df:", weather_df.rdd.getNumPartitions())
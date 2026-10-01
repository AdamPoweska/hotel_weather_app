from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

hotel_schema = StructType([
    StructField("Id", StringType(), True),
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

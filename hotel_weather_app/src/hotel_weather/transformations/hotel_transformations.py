import pygeohash as pgh
from pyspark.sql import DataFrame, SparkSession, functions as F
from pyspark.sql.types import StringType, StructType, StructField, DoubleType


def fill_missing_coordinates(spark: SparkSession, hotels_df: DataFrame, geo_client) -> DataFrame:
    """
    1) "NONE" and empty str are changed into None
    2) missing_rows - collection of rows with missing data
    3) send query to geoapify
    4) geo_schema - small df with results
    5) fill missing values only into main df
    """
    for c in ["Latitude", "Longitude"]:
        hotels_df = hotels_df.withColumn(
            c,
            F.when(F.upper(F.trim(F.col(c).cast("string"))).isin("NONE", ""), None)
            .otherwise(F.col(c))
            .cast("double"),
        )

    missing_rows = (
        hotels_df
        .filter(F.col("Latitude").isNull() | F.col("Longitude").isNull())
        .select("Id", "Name", "Country", "City", "Address")
        .distinct()
        .collect()
    )

    results = []
    for r in missing_rows:
        query = f"{r['Name']} {r['Country']} {r['City']} {r['Address']}"
        coords = geo_client.geocode(query)
        lat, lon = coords if coords is not None else (None, None)
        results.append((r["Id"], lat, lon))

    geo_schema = StructType([
        StructField("Id", hotels_df.schema["Id"].dataType, True),
        StructField("geo_lat", DoubleType(), True),
        StructField("geo_lon", DoubleType(), True),
    ])
    geo_df = spark.createDataFrame(results, schema=geo_schema)

    hotels_df = (
        hotels_df
        .join(geo_df, on="Id", how="left")
        .withColumn("Latitude", F.coalesce("Latitude", "geo_lat"))
        .withColumn("Longitude", F.coalesce("Longitude", "geo_lon"))
        .drop("geo_lat", "geo_lon")
    )
    return hotels_df


@F.udf(returnType=StringType())
def _geohash4_udf(lat, lon):
    if lat is None or lon is None:
        return None
    return pgh.encode(lat, lon, precision=4)


def add_geohash(df: DataFrame, lat_col: str, lon_col: str) -> DataFrame:
    return df.withColumn("geohash", _geohash4_udf(lat_col, lon_col))
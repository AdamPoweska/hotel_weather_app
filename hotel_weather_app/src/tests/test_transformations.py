from pyspark.sql.types import StructType, StructField, StringType, DoubleType

from hotel_weather_app.src.hotel_weather.transformations import add_geohash, fill_missing_coordinates, join_weather_hotels


def test_geohash_has_4_chars_and_known_value(spark):
    # Wikipedia: 57.64911, 10.40744 = "u4pruydqqvj"
    df = spark.createDataFrame([(57.64911, 10.40744)], ["lat", "lng"])
    result = add_geohash(df, "lat", "lng").collect()[0]["geohash"]
    assert result == "u4pr"


def test_geohash_null_for_missing_coordinates(spark):
    schema = StructType([StructField("lat", DoubleType()), StructField("lng", DoubleType())])
    df = spark.createDataFrame([(None, 10.0), (50.0, None)], schema)
    rows = add_geohash(df, "lat", "lng").collect()
    assert all(r["geohash"] is None for r in rows)


class FakeClient:
    """Fake client: known adress gives lat and lon, rest gives None."""
    def __init__(self):
        self.calls = []

    def geocode(self, query):
        self.calls.append(query)
        return (50.0, 19.0) if "Kraków" in query else None


HOTEL_SCHEMA = StructType([
    StructField("Id", StringType()),
    StructField("Name", StringType()),
    StructField("Country", StringType()),
    StructField("City", StringType()),
    StructField("Address", StringType()),
    StructField("Latitude", StringType()),
    StructField("Longitude", StringType()),
])


def test_fill_missing_coordinates(spark):
    df = spark.createDataFrame([
        ("1", "Hotel A", "PL", "Kraków", "ul. A 1", "NONE", "NONE"),
        ("2", "Hotel B", "PL", "Gdańsk", "ul. B 2", "54.3", "18.6"),
        ("3", "Hotel C", "XX", "Nikąd", "ul. C 3", None, None),
    ], HOTEL_SCHEMA)

    client = FakeClient()
    rows = {r["Id"]: r for r in fill_missing_coordinates(spark, df, client).collect()}

    assert (rows["1"]["Latitude"], rows["1"]["Longitude"]) == (50.0, 19.0)
    assert (rows["2"]["Latitude"], rows["2"]["Longitude"]) == (54.3, 18.6)
    assert rows["3"]["Latitude"] is None
    assert len(client.calls) == 2


def test_join_keeps_all_weather_rows_and_does_not_duplicate(spark):
    weather = spark.createDataFrame(
        [(1.0, 2.0, "2017-08-29", "abcd"), (3.0, 4.0, "2017-08-29", "zzzz")],
        ["lng", "lat", "wthr_date", "geohash"])
    hotels = spark.createDataFrame(
        [("1", "Hotel A", "abcd"), ("1", "Hotel A", "abcd")],
        ["Id", "Name", "geohash"])

    result = join_weather_hotels(weather, hotels)

    assert result.count() == 2
    assert result.filter("Id IS NULL").count() == 1
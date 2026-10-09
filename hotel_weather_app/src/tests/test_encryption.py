import base64
import os

import pytest

from hotel_weather_app.src.hotel_weather.encryption import PIIEncryptor

KEY = base64.b64encode(os.urandom(32)).decode()
WRONG_KEY = base64.b64encode(os.urandom(32)).decode()


@pytest.fixture
def df(spark):
    return spark.createDataFrame(
        [("1", "Hotel Stary", "ul. Szczepańska 5", "PL"), ("2", None, None, "PL")],
        ["Id", "Name", "Address", "Country"],
    )


def test_encrypted_columns_differ_and_names_are_preserved(df):
    result = PIIEncryptor(KEY).encrypt(df, ["Name", "Address"])
    assert result.columns == df.columns
    row = result.filter("Id = '1'").collect()[0]
    assert row["Name"] != "Hotel Stary"
    assert row["Address"] != "ul. Szczepańska 5"


def test_non_pii_columns_unchanged(df):
    result = PIIEncryptor(KEY).encrypt(df, ["Name", "Address"])
    assert [r["Country"] for r in result.orderBy("Id").collect()] == ["PL", "PL"]


def test_roundtrip_returns_original(df):
    enc = PIIEncryptor(KEY)
    restored = enc.decrypt(enc.encrypt(df, ["Name", "Address"]), ["Name", "Address"])
    row = restored.filter("Id = '1'").collect()[0]
    assert (row["Name"], row["Address"]) == ("Hotel Stary", "ul. Szczepańska 5")


def test_nulls_stay_null(df):
    result = PIIEncryptor(KEY).encrypt(df, ["Name"])
    assert result.filter("Id = '2'").collect()[0]["Name"] is None


def test_wrong_key_fails(df):
    encrypted = PIIEncryptor(KEY).encrypt(df, ["Name"])
    with pytest.raises(Exception):
        PIIEncryptor(WRONG_KEY).decrypt(encrypted, ["Name"]).collect()


def test_unknown_column_raises(df):
    with pytest.raises(ValueError):
        PIIEncryptor(KEY).encrypt(df, ["Phone"])


def test_invalid_key_length_raises():
    with pytest.raises(ValueError):
        PIIEncryptor(base64.b64encode(b"short").decode())
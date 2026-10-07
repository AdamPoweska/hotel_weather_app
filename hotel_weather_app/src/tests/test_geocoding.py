from unittest.mock import MagicMock, patch
import requests

from hotel_weather_app.src.geo.geoapify import GeoapifyClient


def make_response(status=200, json_data=None):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_data or {}
    resp.raise_for_status.return_value = None
    return resp


def make_client(responses):
    client = GeoapifyClient(api_key="fake", url="https://api.geoapify.com/v1/geocode/search", retries=3)
    client._session = MagicMock()
    client._session.get.side_effect = responses
    return client


def test_geocode_returns_lat_lon():
    client = make_client([make_response(json_data={"results": [{"lat": 50.06, "lon": 19.94}]})])
    assert client.geocode("Hotel Stary Kraków") == (50.06, 19.94)


def test_geocode_returns_none_when_no_results():
    client = make_client([make_response(json_data={"results": []})])
    assert client.geocode("nieistniejący hotel") is None


@patch("hotel_weather_app.src.geo.geoapify.time.sleep")
def test_geocode_retries_on_rate_limit(mock_sleep):
    ok = make_response(json_data={"results": [{"lat": 1.0, "lon": 2.0}]})
    client = make_client([make_response(status=429), ok])
    assert client.geocode("x") == (1.0, 2.0)
    assert client._session.get.call_count == 2


@patch("hotel_weather_app.src.geo.geoapify.time.sleep")
def test_geocode_returns_none_after_all_retries_fail(mock_sleep):
    client = make_client([requests.ConnectionError()] * 3)
    assert client.geocode("x") is None
    assert client._session.get.call_count == 3

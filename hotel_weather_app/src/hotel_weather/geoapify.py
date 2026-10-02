import os
import time
import requests

GEOAPIFY_URL = "https://api.geoapify.com/v1/geocode/search"
API_KEY = os.environ["GEOAPIFY_API_KEY"]

_session = requests.Session()


def geocode(query: str, retries: int = 3) -> tuple[float, float] | None:
    """
    It returns (lat, lon) or None if there is nothing found.
    """
    params = {"text": query, "limit": 1, "format": "json", "apiKey": API_KEY}

    for attempt in range(retries):
        try:
            response = _session.get(GEOAPIFY_URL, params=params, timeout=10)
            if response.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            response.raise_for_status()
            results = response.json().get("results", [])
            if not results:
                return None
            return (results[0]["lat"], results[0]["lon"])
        except requests.RequestException:
            time.sleep(2 ** attempt)
    return None

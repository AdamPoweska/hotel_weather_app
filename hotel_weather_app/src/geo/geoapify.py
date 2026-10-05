import os
import time
import requests


class GeoapifyClient:
    def __init__(self, api_key: str, url: str, retries: int = 3, timeout: int = 10):
        self.api_key = api_key
        self.url = url
        self.retries = retries
        self.timeout = timeout
        self._session = requests.Session()

    def geocode(self, query: str) -> tuple[float, float] | None:
        """
        It returns (lat, lon) or None if there is nothing found.
        """
        params = {"text": query, "limit": 1, "format": "json", "apiKey": self.api_key}

        for attempt in range(self.retries):
            try:
                response = self._session.get(self.url, params=params, timeout=10)
                if response.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                response.raise_for_status()
                results = response.json().get("results", [])
                if not results:
                    return None
                return float(results[0]["lat"]), float(results[0]["lon"])
            except requests.RequestException:
                time.sleep(2 ** attempt)
        return None

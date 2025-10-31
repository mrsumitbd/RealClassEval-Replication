import os
import requests
from typing import Any


class XinyuSearchAPI:
    '''Xinyu Search API Client'''
    DEFAULT_BASE_URL = "https://api.xinyu-search.com/v1"
    DEFAULT_TIMEOUT = 15

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        '''
        Initialize Xinyu Search API client
        Args:
            access_key: Xinyu API access key
            max_results: Maximum number of results to retrieve
        '''
        if not isinstance(access_key, str) or not access_key.strip():
            raise ValueError("access_key must be a non-empty string")
        if not isinstance(search_engine_id, str) or not search_engine_id.strip():
            raise ValueError("search_engine_id must be a non-empty string")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer")

        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results

        self._base_url = os.getenv(
            "XINYU_SEARCH_API_BASE_URL", self.DEFAULT_BASE_URL).rstrip("/")
        self._timeout = float(
            os.getenv("XINYU_SEARCH_API_TIMEOUT", self.DEFAULT_TIMEOUT))

        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Api-Key": self.access_key,
            "User-Agent": "XinyuSearchAPI/1.0",
        })

    def _normalize_results(self, data: Any) -> list[dict]:
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if isinstance(data, dict):
            for key in ("results", "items", "data"):
                if key in data and isinstance(data[key], list):
                    return [item for item in data[key] if isinstance(item, dict)]
        return []

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        payload: dict = dict(body or {})
        payload.setdefault("engine_id", self.search_engine_id)
        payload.setdefault("limit", self.max_results)
        if detail:
            payload["detail"] = True

        url = f"{self._base_url}/search"
        try:
            resp = self._session.post(url, json=payload, timeout=self._timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Xinyu Search API request failed: {e}") from e

        try:
            data = resp.json()
        except ValueError as e:
            raise RuntimeError("Xinyu Search API returned invalid JSON") from e

        return self._normalize_results(data)

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if max_results is not None:
            if not isinstance(max_results, int) or max_results <= 0:
                raise ValueError(
                    "max_results must be a positive integer when provided")

        body = {
            "q": query.strip(),
            "limit": max_results if max_results is not None else self.max_results,
            "engine_id": self.search_engine_id,
        }
        return self.query_detail(body=body, detail=False)

import requests
from typing import Optional, Dict, List


class XinyuSearchAPI:
    """Xinyu Search API Client"""

    DEFAULT_BASE_URL = "https://api.xinyu.ai/v1/search"

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        """
        Initialize Xinyu Search API client
        Args:
            access_key: Xinyu API access key
            max_results: Maximum number of results to retrieve
        """
        if not isinstance(access_key, str) or not access_key.strip():
            raise ValueError("access_key must be a non-empty string")
        if not isinstance(search_engine_id, str) or not search_engine_id.strip():
            raise ValueError("search_engine_id must be a non-empty string")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer")

        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.base_url = self.DEFAULT_BASE_URL
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.access_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "xinyu-search-client/1.0"
        })

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        """
        Query Xinyu search API for detailed results
        Args:
            body: Search parameters
            detail: Whether to get detailed results
        Returns:
            List of search results
        """
        payload: Dict = {}
        if body:
            if not isinstance(body, dict):
                raise ValueError("body must be a dictionary if provided")
            payload.update(body)

        # Ensure required/default params
        payload.setdefault("search_engine_id", self.search_engine_id)
        payload.setdefault("max_results", self.max_results)
        payload["detail"] = bool(detail)

        resp = self._session.post(self.base_url, json=payload, timeout=30)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            # Re-raise with response context
            raise requests.HTTPError(
                f"Xinyu Search API request failed: {e} - {resp.text}") from e

        try:
            data = resp.json()
        except ValueError:
            return []

        return self._extract_results(data)

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        """
        Execute search request
        Args:
            query: Search query
            max_results: Maximum number of results to return
        Returns:
            List of search results
        """
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")

        limit = self.max_results if max_results is None else max_results
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("max_results must be a positive integer")

        body = {
            "query": query,
            "max_results": limit,
        }
        return self.query_detail(body=body, detail=False)

    @staticmethod
    def _extract_results(data: object) -> List[Dict]:
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]

        if isinstance(data, dict):
            # Common top-level keys
            for key in ("results", "items", "data"):
                val = data.get(key)
                if isinstance(val, list):
                    return [item for item in val if isinstance(item, dict)]
                if isinstance(val, dict):
                    # Nested results inside 'data'
                    for subkey in ("results", "items"):
                        subval = val.get(subkey)
                        if isinstance(subval, list):
                            return [item for item in subval if isinstance(item, dict)]
        return []

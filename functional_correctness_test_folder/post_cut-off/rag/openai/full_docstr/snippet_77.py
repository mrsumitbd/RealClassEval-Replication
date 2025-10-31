
import json
import requests
from typing import Any, Dict, List, Optional


class XinyuSearchAPI:
    """Xinyu Search API Client"""

    _BASE_URL = "https://api.xinyu.com/v1/search"

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        """
        Initialize Xinyu Search API client

        Args:
            access_key: Xinyu API access key
            search_engine_id: Identifier for the search engine to use
            max_results: Maximum number of results to retrieve
        """
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self._headers = {
            "Authorization": f"Bearer {self.access_key}",
            "Content-Type": "application/json",
        }

    def _post(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Internal helper to POST to the Xinyu API and return the results list."""
        try:
            response = requests.post(
                self._BASE_URL,
                headers=self._headers,
                data=json.dumps(payload),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            # The API is expected to return a JSON object with a "results" key
            return data.get("results", [])
        except requests.RequestException as exc:
            raise RuntimeError(f"Xinyu API request failed: {exc}") from exc

    def query_detail(self, body: Optional[Dict[str, Any]] = None, detail: bool = True) -> List[Dict[str, Any]]:
        """
        Query Xinyu search API for detailed results

        Args:
            body: Search parameters
            detail: Whether to get detailed results

        Returns:
            List of search results
        """
        if body is None:
            body = {}
        # Ensure required fields are present
        body.setdefault("search_engine_id", self.search_engine_id)
        body.setdefault("detail", detail)
        # Merge max_results if not explicitly set in body
        if "max_results" not in body:
            body["max_results"] = self.max_results
        return self._post(body)

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Execute search request

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            List of search results
        """
        body = {
            "query": query,
            "search_engine_id": self.search_engine_id,
            "detail": True,
        }
        body["max_results"] = max_results if max_results is not None else self.max_results
        return self._post(body)


import json
from typing import Any, Dict, List, Optional

import requests


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
            "Accept": "application/json",
        }

    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Internal helper to POST to the API."""
        try:
            response = requests.post(
                self._BASE_URL,
                headers=self._headers,
                data=json.dumps(payload),
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
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
        body.setdefault("max_results", self.max_results)
        body["detail"] = detail

        result = self._post(body)

        # The API is expected to return a JSON object with a "results" key
        return result.get("results", [])

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Execute search request

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            List of search results
        """
        if max_results is None:
            max_results = self.max_results

        body = {
            "query": query,
            "search_engine_id": self.search_engine_id,
            "max_results": max_results,
            "detail": False,
        }

        return self.query_detail(body=body, detail=False)

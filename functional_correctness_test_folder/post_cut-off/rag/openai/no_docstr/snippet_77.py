import json
import requests
from typing import Dict, List, Optional, Union


class XinyuSearchAPI:
    """Xinyu Search API Client"""

    BASE_URL = "https://api.xinyu.com"

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
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.access_key}",
                "Content-Type": "application/json",
            }
        )

    def _post(self, endpoint: str, payload: Dict) -> Dict:
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.post(url, json=payload)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"Request to {url} failed with status {response.status_code}: {response.text}"
            ) from exc
        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError(f"Invalid JSON response from {url}") from exc

    def query_detail(self, body: Union[Dict, None] = None, detail: bool = True) -> List[Dict]:
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
        body.setdefault("search_engine_id", self.search_engine_id)
        body.setdefault("detail", detail)
        body.setdefault("max_results", self.max_results)

        result = self._post(f"/search/{self.search_engine_id}/detail", body)
        return result.get("results", [])

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict]:
        """
        Execute search request

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            List of search results
        """
        body = {
            "search_engine_id": self.search_engine_id,
            "query": query,
            "detail": False,
            "max_results": max_results or self.max_results,
        }
        result = self._post(f"/search/{self.search_engine_id}/query", body)
        return result.get("results", [])

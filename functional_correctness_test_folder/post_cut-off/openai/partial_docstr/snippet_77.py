
import json
from typing import Any, Dict, List, Optional, Union

import requests


class XinyuSearchAPI:
    """Xinyu Search API Client"""

    def __init__(
        self,
        access_key: str,
        search_engine_id: str,
        max_results: int = 20,
    ):
        """
        Initialize Xinyu Search API client.

        Args:
            access_key: Xinyu API access key.
            search_engine_id: Identifier for the search engine to use.
            max_results: Maximum number of results to retrieve per query.
        """
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.base_url = "https://api.xinyu.com/v1"

    def _request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Internal helper to perform HTTP requests to the Xinyu API.

        Args:
            endpoint: API endpoint path (e.g., "/search/engine_id").
            method: HTTP method ("GET" or "POST").
            data: Payload for POST requests or query parameters for GET.

        Returns:
            Parsed JSON response as a dictionary.

        Raises:
            requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_key}",
            "Content-Type": "application/json",
        }

        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=data)
        else:
            response = requests.post(url, headers=headers, json=data)

        response.raise_for_status()
        return response.json()

    def query_detail(
        self, body: Optional[Dict[str, Any]] = None, detail: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Retrieve detailed search results from the Xinyu API.

        Args:
            body: Optional dictionary containing request parameters.
            detail: If False, returns an empty list without making a request.

        Returns:
            A list of result dictionaries.
        """
        if not detail:
            return []

        if body is None:
            body = {}

        endpoint = f"/search/{self.search_engine_id}/detail"
        response = self._request(endpoint, method="POST", data=body)

        # The API is expected to return a JSON object with a "results" key.
        return response.get("results", [])

    def search(
        self, query: str, max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform a search query against the Xinyu API.

        Args:
            query: The search query string.
            max_results: Optional maximum number of results to return.
                         If None, uses the instance's default.

        Returns:
            A list of result dictionaries.
        """
        if max_results is None:
            max_results = self.max_results

        body = {"query": query, "max_results": max_results}
        return self.query_detail(body=body, detail=True)


import math
import requests
from typing import Any, Dict, List, Optional


class GoogleCustomSearchAPI:
    """Google Custom Search API Client"""

    def __init__(
        self,
        api_key: str,
        search_engine_id: str,
        max_results: int = 20,
        num_per_request: int = 10,
    ):
        """
        Initialize Google Custom Search API client

        Args:
            api_key: Google API key
            search_engine_id: Search engine ID (cx parameter)
            max_results: Maximum number of results to retrieve
            num_per_request: Number of results per API request
        """
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.num_per_request = num_per_request
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(
        self,
        query: str,
        num_results: Optional[int] = None,
        start_index: int = 1,
    ) -> Dict[str, Any]:
        """
        Execute search request

        Args:
            query: Search query
            num_results: Number of results to return (uses config default if None)
            start_index: Starting index (default 1)

        Returns:
            Dictionary containing search results
        """
        if num_results is None:
            num_results = self.max_results
        if num_results <= 0:
            raise ValueError("num_results must be positive")
        if start_index <= 0:
            raise ValueError("start_index must be positive")

        # Google API limits num to 10 per request
        num = min(self.num_per_request, num_results)

        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "start": start_index,
            "num": num,
        }

        response = requests.get(self.base_url, params=params)
        if response.status_code != 200:
            raise RuntimeError(
                f"Google Custom Search API error {response.status_code}: {response.text}"
            )
        return response.json()

    def get_all_results(
        self, query: str, max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all search results (with pagination)

        Args:
            query: Search query
            max_results: Maximum number of results (uses config default if None)

        Returns:
            List of all search results
        """
        if max_results is None:
            max_results = self.max_results
        if max_results <= 0:
            raise ValueError("max_results must be positive")

        results: List[Dict[str, Any]] = []
        start_index = 1
        remaining = max_results

        while remaining > 0:
            # Determine how many to request this round
            num_to_fetch = min(self.num_per_request, remaining)
            response = self.search(query, num_to_fetch, start_index)

            items = response.get("items", [])
            if not items:
                break

            results.extend(items)
            fetched = len(items)
            remaining -= fetched
            start_index += fetched

            # If fewer items returned than requested, no more results
            if fetched < num_to_fetch:
                break

        return results

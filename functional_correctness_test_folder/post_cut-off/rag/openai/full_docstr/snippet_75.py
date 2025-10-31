
import math
import requests
from typing import Any, Dict, List, Optional, Union


class GoogleCustomSearchAPI:
    """Google Custom Search API Client"""

    BASE_URL = "https://www.googleapis.com/customsearch/v1"

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
        if not api_key:
            raise ValueError("api_key must be provided")
        if not search_engine_id:
            raise ValueError("search_engine_id must be provided")
        if max_results <= 0:
            raise ValueError("max_results must be positive")
        if num_per_request <= 0:
            raise ValueError("num_per_request must be positive")
        if num_per_request > max_results:
            raise ValueError(
                "num_per_request cannot be greater than max_results"
            )

        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.num_per_request = num_per_request

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
        if not query:
            raise ValueError("query must be provided")

        # Determine how many results to request
        num_results = num_results if num_results is not None else self.max_results
        if num_results <= 0:
            raise ValueError("num_results must be positive")
        if num_results > self.max_results:
            num_results = self.max_results

        # Google API limits num to 10 per request
        num = min(self.num_per_request, num_results)

        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "start": start_index,
            "num": num,
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
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
        if not query:
            raise ValueError("query must be provided")

        max_results = max_results if max_results is not None else self.max_results
        if max_results <= 0:
            raise ValueError("max_results must be positive")
        if max_results > self.max_results:
            max_results = self.max_results

        results: List[Dict[str, Any]] = []
        start_index = 1
        remaining = max_results

        while remaining > 0:
            # Determine how many to request in this batch
            batch_size = min(self.num_per_request, remaining)
            response = self.search(
                query, num_results=batch_size, start_index=start_index)
            items = response.get("items", [])
            if not items:
                break  # No more results

            results.extend(items)
            fetched = len(items)
            remaining -= fetched
            start_index += fetched

            # Google API caps at 100 results total
            if start_index > 100:
                break

        return results

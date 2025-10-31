
import requests
from typing import List, Dict, Optional, Union


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
        # Google Custom Search API limits num to 10 per request
        self.num_per_request = min(num_per_request, 10)
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(
        self,
        query: str,
        num_results: Optional[int] = None,
        start_index: int = 1,
    ) -> Dict:
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
            raise ValueError("Query must not be empty")

        # Determine number of results for this request
        requested = num_results if num_results is not None else self.max_results
        # Cap to the maximum allowed per request
        num = min(requested, self.num_per_request)

        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "start": start_index,
            "num": num,
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_all_results(
        self, query: str, max_results: Optional[int] = None
    ) -> List[Dict]:
        """
        Get all search results (with pagination)

        Args:
            query: Search query
            max_results: Maximum number of results (uses config default if None)

        Returns:
            List of all search results
        """
        if not query:
            raise ValueError("Query must not be empty")

        target = max_results if max_results is not None else self.max_results
        results: List[Dict] = []
        start_index = 1

        while len(results) < target:
            # Determine how many results we still need
            remaining = target - len(results)
            # Use the smaller of remaining and num_per_request
            num_to_fetch = min(remaining, self.num_per_request)

            # Perform the search
            page = self.search(query, num_results=num_to_fetch,
                               start_index=start_index)

            # Extract items; if none, break
            items = page.get("items", [])
            if not items:
                break

            results.extend(items)

            # Prepare for next page
            start_index += self.num_per_request

            # If the API returned fewer items than requested, no more pages
            if len(items) < num_to_fetch:
                break

        return results[:target]

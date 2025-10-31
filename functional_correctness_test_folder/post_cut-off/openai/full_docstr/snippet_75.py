
import requests
from typing import List, Dict, Optional, Union


class GoogleCustomSearchAPI:
    '''Google Custom Search API Client'''

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
        # Google Custom Search API allows a maximum of 10 results per request
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
        if num_results is None:
            num_results = self.max_results
        # Google API limits num to 10
        num = min(num_results, self.num_per_request)
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
        if max_results is None:
            max_results = self.max_results

        results: List[Dict] = []
        start_index = 1

        while len(results) < max_results:
            # Determine how many results to request in this batch
            remaining = max_results - len(results)
            batch_size = min(remaining, self.num_per_request)

            # Google Custom Search API only supports start indices up to 100
            if start_index > 100:
                break

            response = self.search(
                query, num_results=batch_size, start_index=start_index)
            items = response.get("items", [])
            if not items:
                break

            results.extend(items)

            # If fewer items than requested, no more results are available
            if len(items) < batch_size:
                break

            start_index += batch_size

        return results

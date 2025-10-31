
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
        Initialize the client.

        Args:
            api_key: Google API key.
            search_engine_id: Custom Search Engine ID (cx).
            max_results: Default maximum number of results to return.
            num_per_request: Maximum number of results per single API request
                (Google limits this to 10).
        """
        if not api_key:
            raise ValueError("api_key must be provided")
        if not search_engine_id:
            raise ValueError("search_engine_id must be provided")
        if max_results <= 0:
            raise ValueError("max_results must be positive")
        if not (1 <= num_per_request <= 10):
            raise ValueError("num_per_request must be between 1 and 10")

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
    ) -> Dict:
        """
        Execute a single search request.

        Args:
            query: Search query.
            num_results: Number of results to return for this request.
                If None, uses the client's default max_results.
            start_index: Starting index for the search results (1-based).

        Returns:
            Dictionary containing the JSON response from the API.
        """
        if not query:
            raise ValueError("query must be provided")

        if start_index < 1:
            raise ValueError("start_index must be >= 1")

        # Determine how many results to request in this call
        if num_results is None:
            num_results = self.max_results
        if num_results <= 0:
            raise ValueError("num_results must be positive")

        # Google limits num to 10 per request
        num_to_request = min(self.num_per_request, num_results)

        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "start": start_index,
            "num": num_to_request,
        }

        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_all_results(
        self, query: str, max_results: Optional[int] = None
    ) -> List[Dict]:
        """
        Retrieve all search results for a query, handling pagination.

        Args:
            query: Search query.
            max_results: Maximum number of results to return.
                If None, uses the client's default max_results.

        Returns:
            List of result items (each item is a dict).
        """
        if not query:
            raise ValueError("query must be provided")

        if max_results is None:
            max_results = self.max_results
        if max_results <= 0:
            raise ValueError("max_results must be positive")

        results: List[Dict] = []
        start_index = 1

        while len(results) < max_results:
            remaining = max_results - len(results)
            # The API will return at most num_per_request items per call
            # but we pass the remaining count so that search() limits itself
            response = self.search(
                query, num_results=remaining, start_index=start_index)

            items = response.get("items", [])
            if not items:
                break

            results.extend(items)

            # Determine next start index if available
            queries = response.get("queries", {})
            next_pages = queries.get("nextPage", [])
            if next_pages:
                next_start = next_pages[0].get("startIndex")
                if next_start and next_start > start_index:
                    start_index = next_start
                else:
                    break
            else:
                break

        return results

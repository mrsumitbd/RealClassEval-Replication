
import requests
from typing import Dict, List, Optional, Union


class GoogleCustomSearchAPI:
    """Google Custom Search API Client"""

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):
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
        self.base_url = 'https://www.googleapis.com/customsearch/v1'

    def search(self, query: str, num_results: Optional[int] = None, start_index: int = 1) -> Dict:
        """
        Execute search request

        Args:
            query: Search query
            num_results: Number of results to return (uses config default if None)
            start_index: Starting index (default 1)

        Returns:
            Dictionary containing search results
        """
        num_results = num_results or self.num_per_request
        num_results = min(num_results, self.num_per_request)
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': num_results,
            'start': start_index
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_all_results(self, query: str, max_results: Optional[int] = None) -> List[Dict]:
        """
        Get all search results (with pagination)

        Args:
            query: Search query
            max_results: Maximum number of results (uses config default if None)

        Returns:
            List of all search results
        """
        max_results = max_results or self.max_results
        results = []
        start_index = 1
        while len(results) < max_results:
            num_results = min(self.num_per_request, max_results - len(results))
            response = self.search(query, num_results, start_index)
            results.extend(response.get('items', []))
            if 'nextPage' not in response.get('queries', {}):
                break
            start_index = response['queries']['nextPage'][0]['startIndex']
        return results[:max_results]

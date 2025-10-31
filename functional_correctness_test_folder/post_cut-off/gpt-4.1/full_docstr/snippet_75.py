
import requests


class GoogleCustomSearchAPI:
    '''Google Custom Search API Client'''

    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):
        '''
        Initialize Google Custom Search API client
        Args:
            api_key: Google API key
            search_engine_id: Search engine ID (cx parameter)
            max_results: Maximum number of results to retrieve
            num_per_request: Number of results per API request
        '''
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        # Google API allows max 10 per request
        self.num_per_request = min(max(1, num_per_request), 10)

    def search(self, query: str, num_results: int | None = None, start_index: int = 1) -> dict:
        '''
        Execute search request
        Args:
            query: Search query
            num_results: Number of results to return (uses config default if None)
            start_index: Starting index (default 1)
        Returns:
            Dictionary containing search results
        '''
        if num_results is None:
            num_results = self.num_per_request
        # Google API allows max 10 per request
        num_results = min(max(1, num_results), 10)

        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': num_results,
            'start': start_index
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    def get_all_results(self, query: str, max_results: int | None = None) -> list[dict]:
        '''
        Get all search results (with pagination)
        Args:
            query: Search query
            max_results: Maximum number of results (uses config default if None)
        Returns:
            List of all search results
        '''
        if max_results is None:
            max_results = self.max_results
        results = []
        start_index = 1
        remaining = max_results

        while remaining > 0:
            num_to_fetch = min(self.num_per_request, remaining)
            data = self.search(query, num_results=num_to_fetch,
                               start_index=start_index)
            items = data.get('items', [])
            if not items:
                break
            results.extend(items)
            fetched = len(items)
            if fetched < num_to_fetch:
                break
            remaining -= fetched
            start_index += fetched
        return results

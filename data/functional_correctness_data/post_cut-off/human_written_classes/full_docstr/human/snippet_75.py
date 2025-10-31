import requests

class GoogleCustomSearchAPI:
    """Google Custom Search API Client"""

    def __init__(self, api_key: str, search_engine_id: str, max_results: int=20, num_per_request: int=10):
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
        self.num_per_request = min(num_per_request, 10)
        self.base_url = 'https://www.googleapis.com/customsearch/v1'

    def search(self, query: str, num_results: int | None=None, start_index: int=1) -> dict:
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
            num_results = self.num_per_request
        params = {'key': self.api_key, 'cx': self.search_engine_id, 'q': query, 'num': min(num_results, self.num_per_request), 'start': start_index}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Google search request failed: {e}')
            return {}

    def get_all_results(self, query: str, max_results: int | None=None) -> list[dict]:
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
        all_results = []
        start_index = 1
        while len(all_results) < max_results:
            search_data = self.search(query, start_index=start_index)
            if not search_data or 'items' not in search_data:
                break
            all_results.extend(search_data['items'])
            if len(search_data['items']) < self.num_per_request:
                break
            start_index += self.num_per_request
            if start_index > 100:
                break
        return all_results[:max_results]
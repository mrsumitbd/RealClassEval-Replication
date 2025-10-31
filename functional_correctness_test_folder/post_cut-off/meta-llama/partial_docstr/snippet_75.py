
import requests


class GoogleCustomSearchAPI:
    '''Google Custom Search API Client'''

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.num_per_request = num_per_request
        self.base_url = "https://www.googleapis.com/customsearch/v1"

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
        num_results = min(num_results, self.num_per_request)

        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": num_results,
            "start": start_index
        }

        response = requests.get(self.base_url, params=params)
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

        while len(results) < max_results:
            num_results = min(max_results - len(results), self.num_per_request)
            response = self.search(query, num_results, start_index)

            if 'items' not in response:
                break

            results.extend(response['items'])
            start_index += len(response['items'])

            if len(response['items']) < num_results:
                break

        return results[:max_results]

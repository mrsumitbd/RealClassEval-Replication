
import requests
from typing import Union, List, Dict


class GoogleCustomSearchAPI:
    '''Google Custom Search API Client'''

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
        self.num_per_request = num_per_request
        self.base_url = 'https://www.googleapis.com/customsearch/v1'

    def search(self, query: str, num_results: Union[int, None] = None, start_index: int = 1) -> dict:
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

    def get_all_results(self, query: str, max_results: Union[int, None] = None) -> List[dict]:
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

        all_results = []
        start_index = 1
        remaining_results = max_results

        while remaining_results > 0:
            num_results = min(remaining_results, self.num_per_request)
            results = self.search(query, num_results, start_index)

            if 'items' not in results:
                break

            all_results.extend(results['items'])
            remaining_results -= len(results['items'])
            start_index += num_results

            if 'nextPage' not in results.get('queries', {}):
                break

        return all_results

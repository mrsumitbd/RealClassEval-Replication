
import requests
from typing import Optional, Union, List, Dict


class XinyuSearchAPI:
    '''Xinyu Search API Client'''

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        '''
        Initialize Xinyu Search API client
        Args:
            access_key: Xinyu API access key
            max_results: Maximum number of results to retrieve
        '''
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.base_url = "https://api.xinyu.com/v1/search"

    def query_detail(self, body: Optional[Union[dict, None]] = None, detail: bool = True) -> List[Dict]:
        '''
        Query Xinyu search API for detailed results
        Args:
            body: Search parameters
            detail: Whether to get detailed results
        Returns:
            List of search results
        '''
        if body is None:
            body = {}
        body['detail'] = detail
        headers = {
            'Authorization': f'Bearer {self.access_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(
            f"{self.base_url}/{self.search_engine_id}",
            json=body,
            headers=headers
        )
        response.raise_for_status()
        return response.json().get('results', [])

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict]:
        '''
        Execute search request
        Args:
            query: Search query
            max_results: Maximum number of results to return
        Returns:
            List of search results
        '''
        if max_results is None:
            max_results = self.max_results
        body = {
            'query': query,
            'max_results': max_results
        }
        return self.query_detail(body)

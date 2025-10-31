
import requests


class XinyuSearchAPI:
    '''Xinyu Search API Client'''

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        '''
        Initialize Xinyu Search API client
        Args:
            access_key: Xinyu API access key
            search_engine_id: ID of the search engine to use
            max_results: Maximum number of results to retrieve
        '''
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.base_url = "https://api.xinyusearch.com/v1"

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
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
        body['max_results'] = self.max_results
        headers = {
            'Authorization': f'Bearer {self.access_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(
            f"{self.base_url}/search/{self.search_engine_id}/query", json=body, headers=headers)
        response.raise_for_status()
        return response.json().get('results', [])

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
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
        return self.query_detail(body, detail=False)

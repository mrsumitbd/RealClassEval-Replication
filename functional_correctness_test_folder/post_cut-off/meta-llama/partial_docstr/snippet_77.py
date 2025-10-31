
import requests


class XinyuSearchAPI:
    '''Xinyu Search API Client'''

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        '''
        Initialize Xinyu Search API client
        Args:
            access_key: Xinyu API access key
            search_engine_id: Xinyu search engine ID
            max_results: Maximum number of results to retrieve
        '''
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.base_url = 'https://api.xinyu.com/search'

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        if body is None:
            body = {}
        headers = {
            'Authorization': f'Bearer {self.access_key}',
            'Content-Type': 'application/json'
        }
        params = {
            'engine_id': self.search_engine_id,
            'detail': str(detail).lower()
        }
        response = requests.post(
            self.base_url + '/query', headers=headers, json=body, params=params)
        response.raise_for_status()
        return response.json()

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        max_results = max_results or self.max_results
        body = {
            'query': query,
            'max_results': max_results
        }
        return self.query_detail(body)

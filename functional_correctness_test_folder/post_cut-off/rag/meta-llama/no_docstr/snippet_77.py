
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
        self.base_url = "https://api.xinyu.com/search"

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
        body["access_key"] = self.access_key
        body["search_engine_id"] = self.search_engine_id
        body["detail"] = detail
        response = requests.post(self.base_url, json=body)
        response.raise_for_status()
        return response.json()

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
            "query": query,
            "max_results": max_results
        }
        return self.query_detail(body)


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
        body["search_engine_id"] = self.search_engine_id
        body["detail"] = detail
        headers = {"Authorization": f"Bearer {self.access_key}"}
        response = requests.post(self.base_url, json=body, headers=headers)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            raise Exception(
                f"Failed to retrieve search results: {response.text}")

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
        body = {"query": query, "max_results": max_results}
        return self.query_detail(body)


import requests


class XinyuSearchAPI:
    '''Xinyu Search API Client'''

    BASE_URL = "https://api.xinyu.com/v1/search"

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
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_key}",
            "Content-Type": "application/json"
        })

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
        body = body.copy()
        body["search_engine_id"] = self.search_engine_id
        body["max_results"] = body.get("max_results", self.max_results)
        body["detail"] = detail

        response = self.session.post(self.BASE_URL, json=body)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        '''
        Execute search request
        Args:
            query: Search query
            max_results: Maximum number of results to return
        Returns:
            List of search results
        '''
        params = {
            "query": query,
            "search_engine_id": self.search_engine_id,
            "max_results": max_results if max_results is not None else self.max_results,
            "detail": False
        }
        response = self.session.post(self.BASE_URL, json=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])

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
        params = {
            "access_key": self.access_key,
            "engine_id": self.search_engine_id,
            "max_results": body.get("max_results", self.max_results),
            "detail": "true" if detail else "false"
        }
        if "query" in body:
            params["query"] = body["query"]
        params.update({k: v for k, v in body.items(
        ) if k not in params and k != "max_results" and k != "query"})
        response = requests.get(self.BASE_URL, params=params)
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
            "access_key": self.access_key,
            "engine_id": self.search_engine_id,
            "query": query,
            "max_results": max_results if max_results is not None else self.max_results,
            "detail": "false"
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])

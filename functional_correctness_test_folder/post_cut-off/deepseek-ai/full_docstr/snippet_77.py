
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

        headers = {
            "Authorization": f"Bearer {self.access_key}",
            "Content-Type": "application/json"
        }

        params = {
            "detail": str(detail).lower(),
            "max_results": self.max_results
        }

        response = requests.post(
            f"{self.base_url}/query_detail",
            headers=headers,
            json=body,
            params=params
        )

        response.raise_for_status()
        return response.json().get("results", [])

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        '''
        Execute search request
        Args:
            query: Search query
            max_results: Maximum number of results to return
        Returns:
            List of search results
        '''
        headers = {
            "Authorization": f"Bearer {self.access_key}",
            "Content-Type": "application/json"
        }

        params = {
            "q": query,
            "max_results": max_results if max_results is not None else self.max_results,
            "engine_id": self.search_engine_id
        }

        response = requests.get(
            f"{self.base_url}/search",
            headers=headers,
            params=params
        )

        response.raise_for_status()
        return response.json().get("results", [])

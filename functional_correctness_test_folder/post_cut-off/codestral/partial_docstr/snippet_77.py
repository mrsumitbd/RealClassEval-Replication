
import requests


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

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        headers = {
            "Authorization": f"Bearer {self.access_key}",
            "Content-Type": "application/json"
        }
        params = {
            "detail": detail
        }
        response = requests.post(
            f"{self.base_url}/query", headers=headers, params=params, json=body)
        response.raise_for_status()
        return response.json()

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        if max_results is None:
            max_results = self.max_results
        headers = {
            "Authorization": f"Bearer {self.access_key}",
            "Content-Type": "application/json"
        }
        params = {
            "q": query,
            "num": max_results,
            "search_engine_id": self.search_engine_id
        }
        response = requests.get(
            f"{self.base_url}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

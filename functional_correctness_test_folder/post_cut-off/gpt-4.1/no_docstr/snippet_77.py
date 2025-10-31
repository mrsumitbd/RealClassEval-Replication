
import requests


class XinyuSearchAPI:

    BASE_URL = "https://api.xinyusearch.com/v1/search"

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        if body is None:
            body = {}
        params = {
            "access_key": self.access_key,
            "engine_id": self.search_engine_id,
            "detail": "true" if detail else "false",
        }
        params.update(body)
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        if max_results is None:
            max_results = self.max_results
        body = {
            "q": query,
            "num": max_results
        }
        return self.query_detail(body=body, detail=True)

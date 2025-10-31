
import requests


class XinyuSearchAPI:

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        if body is None:
            body = {}
        body['key'] = self.access_key
        body['cx'] = self.search_engine_id
        response = requests.get(self.base_url, params=body)
        if response.status_code == 200:
            results = response.json().get('items', [])
            if detail:
                return results
            else:
                return [{'title': item.get('title'), 'link': item.get('link')} for item in results]
        else:
            raise Exception(f"Error: {response.status_code}")

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        if max_results is None:
            max_results = self.max_results
        body = {
            'q': query,
            'num': max_results
        }
        return self.query_detail(body)

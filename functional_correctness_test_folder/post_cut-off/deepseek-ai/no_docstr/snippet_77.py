
import requests
from typing import Optional, Union


class XinyuSearchAPI:

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def query_detail(self, body: Optional[dict] = None, detail: bool = True) -> list[dict]:
        if body is None:
            body = {}

        params = {
            'key': self.access_key,
            'cx': self.search_engine_id,
        }
        params.update(body)

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        if 'items' in data:
            for item in data['items']:
                result = {
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                }
                if detail:
                    result.update({
                        'displayLink': item.get('displayLink', ''),
                        'formattedUrl': item.get('formattedUrl', ''),
                    })
                results.append(result)
        return results

    def search(self, query: str, max_results: Optional[int] = None) -> list[dict]:
        if max_results is None:
            max_results = self.max_results

        body = {
            'q': query,
            'num': max_results,
        }
        return self.query_detail(body)

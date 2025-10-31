
import requests


class GoogleCustomSearchAPI:

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.num_per_request = num_per_request

    def search(self, query: str, num_results: int | None = None, start_index: int = 1) -> dict:
        if num_results is None:
            num_results = self.max_results
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': query,
            'key': self.api_key,
            'cx': self.search_engine_id,
            'num': min(num_results, self.num_per_request),
            'start': start_index
        }
        response = requests.get(url, params=params)
        return response.json()

    def get_all_results(self, query: str, max_results: int | None = None) -> list[dict]:
        if max_results is None:
            max_results = self.max_results
        all_results = []
        start_index = 1
        while len(all_results) < max_results:
            response = self.search(
                query, num_results=max_results, start_index=start_index)
            items = response.get('items', [])
            if not items:
                break
            all_results.extend(items)
            start_index += len(items)
            if 'queries' in response and 'nextPage' in response['queries']:
                start_index = response['queries']['nextPage'][0]['startIndex']
            else:
                break
        return all_results[:max_results]

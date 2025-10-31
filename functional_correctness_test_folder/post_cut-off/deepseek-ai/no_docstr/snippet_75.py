
import requests


class GoogleCustomSearchAPI:

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.num_per_request = num_per_request

    def search(self, query: str, num_results: int | None = None, start_index: int = 1) -> dict:
        if num_results is None:
            num_results = self.num_per_request

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'start': start_index,
            'num': min(num_results, self.num_per_request)
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_all_results(self, query: str, max_results: int | None = None) -> list[dict]:
        if max_results is None:
            max_results = self.max_results

        results = []
        remaining = max_results
        start_index = 1

        while remaining > 0:
            num_to_fetch = min(remaining, self.num_per_request)
            response = self.search(
                query, num_results=num_to_fetch, start_index=start_index)
            items = response.get('items', [])
            results.extend(items)

            remaining -= len(items)
            start_index += len(items)

            if len(items) < num_to_fetch:
                break

        return results

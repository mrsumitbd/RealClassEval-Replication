
import requests


class GoogleCustomSearchAPI:

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):

        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.num_per_request = num_per_request
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(self, query: str, num_results: int | None = None, start_index: int = 1) -> dict:

        if num_results is None:
            num_results = self.num_per_request

        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': num_results,
            'start': start_index
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()

        return response.json()

    def get_all_results(self, query: str, max_results: int | None = None) -> list[dict]:

        if max_results is None:
            max_results = self.max_results

        all_results = []
        start_index = 1

        while len(all_results) < max_results:
            results = self.search(query, min(
                self.num_per_request, max_results - len(all_results)), start_index)

            if 'items' not in results:
                break

            all_results.extend(results['items'])
            start_index += self.num_per_request

        return all_results[:max_results]


import requests


class GoogleCustomSearchAPI:

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        # Google API allows max 10 per request
        self.num_per_request = min(max(1, num_per_request), 10)
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(self, query: str, num_results: int | None = None, start_index: int = 1) -> dict:
        if num_results is None:
            num_results = self.num_per_request
        # Google API allows max 10 per request
        num_results = min(max(1, num_results), 10)
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "start": start_index,
            "num": num_results,
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_all_results(self, query: str, max_results: int | None = None) -> list[dict]:
        results = []
        total_to_fetch = max_results if max_results is not None else self.max_results
        start_index = 1
        while len(results) < total_to_fetch:
            num_to_fetch = min(self.num_per_request,
                               total_to_fetch - len(results))
            data = self.search(query, num_results=num_to_fetch,
                               start_index=start_index)
            items = data.get("items", [])
            if not items:
                break
            results.extend(items)
            start_index += len(items)
            if len(items) < num_to_fetch:
                break  # No more results available
        return results[:total_to_fetch]

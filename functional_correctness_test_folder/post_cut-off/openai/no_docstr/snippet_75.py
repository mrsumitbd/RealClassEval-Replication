
import requests
from typing import List, Dict, Optional, Union


class GoogleCustomSearchAPI:
    """
    A simple wrapper around the Google Custom Search JSON API.
    """

    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(
        self,
        api_key: str,
        search_engine_id: str,
        max_results: int = 20,
        num_per_request: int = 10,
    ):
        """
        Initialize the API client.

        :param api_key: Google API key.
        :param search_engine_id: Custom Search Engine ID (cx).
        :param max_results: Maximum number of results to return in a single search call.
        :param num_per_request: Number of results to request per API call (max 10).
        """
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.num_per_request = min(max(1, num_per_request), 10)

    def _build_params(
        self,
        query: str,
        num: int,
        start: int,
    ) -> Dict[str, Union[str, int]]:
        return {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": num,
            "start": start,
        }

    def search(
        self,
        query: str,
        num_results: Optional[int] = None,
        start_index: int = 1,
    ) -> Dict:
        """
        Perform a single search request.

        :param query: Search query string.
        :param num_results: Number of results to request (max 10). If None, uses self.num_per_request.
        :param start_index: Index of the first result to return (1-based).
        :return: JSON response as a dictionary.
        :raises RuntimeError: If the API request fails.
        """
        if num_results is None:
            num = self.num_per_request
        else:
            num = min(max(1, num_results), 10)

        params = self._build_params(query, num, start_index)

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(
                f"Google Custom Search API request failed: {exc}") from exc

        return response.json()

    def get_all_results(
        self,
        query: str,
        max_results: Optional[int] = None,
    ) -> List[Dict]:
        """
        Retrieve up to max_results results for the given query, handling pagination.

        :param query: Search query string.
        :param max_results: Maximum number of results to return. If None, uses self.max_results.
        :return: List of result items (each item is a dict).
        """
        if max_results is None:
            max_results = self.max_results

        results: List[Dict] = []
        start_index = 1

        while len(results) < max_results:
            remaining = max_results - len(results)
            num_to_fetch = min(self.num_per_request, remaining)

            response = self.search(
                query, num_results=num_to_fetch, start_index=start_index)

            items = response.get("items", [])
            if not items:
                break

            results.extend(items)

            # Google API returns at most 10 results per request; if fewer items returned,
            # we assume no more results are available.
            if len(items) < num_to_fetch:
                break

            start_index += len(items)

        return results[:max_results]

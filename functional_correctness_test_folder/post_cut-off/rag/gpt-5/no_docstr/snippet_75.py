import time
from typing import Any, Dict, List, Optional

import requests


class GoogleCustomSearchAPI:
    """Google Custom Search API Client"""

    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(
        self,
        api_key: str,
        search_engine_id: str,
        max_results: int = 20,
        num_per_request: int = 10,
    ):
        """
        Initialize Google Custom Search API client
        Args:
            api_key: Google API key
            search_engine_id: Search engine ID (cx parameter)
            max_results: Maximum number of results to retrieve
            num_per_request: Number of results per API request
        """
        if not api_key or not isinstance(api_key, str):
            raise ValueError("api_key must be a non-empty string.")
        if not search_engine_id or not isinstance(search_engine_id, str):
            raise ValueError("search_engine_id must be a non-empty string.")
        if not isinstance(max_results, int) or max_results < 1:
            raise ValueError("max_results must be a positive integer.")
        if not isinstance(num_per_request, int) or not (1 <= num_per_request <= 10):
            raise ValueError(
                "num_per_request must be an integer between 1 and 10 (inclusive).")

        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.num_per_request = num_per_request
        self._timeout = 15
        self._max_retries = 3

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "GoogleCustomSearchAPI/1.0",
            }
        )

    def _call_api(self, params: Dict[str, Any]) -> Dict[str, Any]:
        last_error: Optional[Exception] = None
        for attempt in range(self._max_retries + 1):
            try:
                resp = self._session.get(
                    self.BASE_URL, params=params, timeout=self._timeout)
                if resp.status_code == 200:
                    return resp.json()
                # Retry on transient errors
                if resp.status_code in (429, 500, 502, 503, 504):
                    # Exponential backoff
                    delay = min(2 ** attempt, 10)
                    time.sleep(delay)
                    continue
                # Non-retryable errors
                try:
                    payload = resp.json()
                    message = payload.get("error", {}).get(
                        "message") or resp.text
                except Exception:
                    message = resp.text
                resp.raise_for_status()  # Will raise HTTPError
            except requests.RequestException as e:
                last_error = e
                # Retry network-level issues
                delay = min(2 ** attempt, 10)
                time.sleep(delay)
                continue
        # Exhausted retries
        if last_error:
            raise RuntimeError(
                f"Failed to call Google Custom Search API: {last_error}") from last_error
        raise RuntimeError(
            "Failed to call Google Custom Search API due to unknown error.")

    def search(self, query: str, num_results: int | None = None, start_index: int = 1) -> dict:
        """
        Execute search request
        Args:
            query: Search query
            num_results: Number of results to return (uses config default if None)
            start_index: Starting index (default 1)
        Returns:
            Dictionary containing search results
        """
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string.")
        if not isinstance(start_index, int) or start_index < 1:
            raise ValueError("start_index must be an integer >= 1.")
        if start_index > 100:
            raise ValueError(
                "start_index cannot exceed 100 due to API limits.")

        num = self.num_per_request if num_results is None else num_results
        if not isinstance(num, int) or num < 1:
            raise ValueError("num_results must be a positive integer.")
        # Google CSE allows a maximum of 10 results per single request
        num = min(num, 10)

        params: Dict[str, Any] = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": num,
            "start": start_index,
        }
        return self._call_api(params)

    def get_all_results(self, query: str, max_results: int | None = None) -> list[dict]:
        """
        Get all search results (with pagination)
        Args:
            query: Search query
            max_results: Maximum number of results (uses config default if None)
        Returns:
            List of all search results
        """
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string.")

        max_fetch = self.max_results if max_results is None else max_results
        if not isinstance(max_fetch, int) or max_fetch < 1:
            raise ValueError("max_results must be a positive integer.")
        # Google CSE only returns up to 100 results
        max_fetch = min(max_fetch, 100)

        results: List[Dict[str, Any]] = []
        start = 1

        while len(results) < max_fetch and start <= 100:
            remaining = max_fetch - len(results)
            to_fetch = min(self.num_per_request, remaining, 10)
            data = self.search(
                query=query, num_results=to_fetch, start_index=start)
            items = data.get("items", []) or []
            if not items:
                break
            results.extend(items)
            start += len(items)
            if start > 100:
                break

            # Optional: Respect nextPage if present
            next_page = (
                data.get("queries", {})
                .get("nextPage", [{}])[0]
                .get("startIndex")
            )
            if isinstance(next_page, int) and next_page > start:
                start = next_page

        return results

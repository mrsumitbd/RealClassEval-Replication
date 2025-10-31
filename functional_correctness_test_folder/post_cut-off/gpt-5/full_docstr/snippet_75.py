import requests
from typing import Optional, List, Dict


class GoogleCustomSearchAPI:
    '''Google Custom Search API Client'''

    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):
        '''
        Initialize Google Custom Search API client
        Args:
            api_key: Google API key
            search_engine_id: Search engine ID (cx parameter)
            max_results: Maximum number of results to retrieve
            num_per_request: Number of results per API request
        '''
        if not api_key or not isinstance(api_key, str):
            raise ValueError("api_key must be a non-empty string")
        if not search_engine_id or not isinstance(search_engine_id, str):
            raise ValueError("search_engine_id must be a non-empty string")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer")
        if not isinstance(num_per_request, int) or num_per_request <= 0:
            raise ValueError("num_per_request must be a positive integer")

        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.num_per_request = min(num_per_request, 10)
        self.session = requests.Session()

    def search(self, query: str, num_results: Optional[int] = None, start_index: int = 1) -> Dict:
        '''
        Execute search request
        Args:
            query: Search query
            num_results: Number of results to return (uses config default if None)
            start_index: Starting index (default 1)
        Returns:
            Dictionary containing search results
        '''
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")

        if num_results is None:
            num = self.num_per_request
        else:
            if not isinstance(num_results, int) or num_results <= 0:
                raise ValueError("num_results must be a positive integer")
            num = min(num_results, 10)

        if not isinstance(start_index, int) or start_index < 1:
            raise ValueError("start_index must be an integer >= 1")

        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": num,
            "start": start_index,
        }

        resp = self.session.get(self.BASE_URL, params=params, timeout=30)
        if resp.status_code != 200:
            # Try to include error details if present
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            raise requests.HTTPError(
                f"Google CSE API error {resp.status_code}: {detail}", response=resp)

        return resp.json()

    def get_all_results(self, query: str, max_results: Optional[int] = None) -> List[Dict]:
        '''
        Get all search results (with pagination)
        Args:
            query: Search query
            max_results: Maximum number of results (uses config default if None)
        Returns:
            List of all search results
        '''
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")

        limit = self.max_results if max_results is None else max_results
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("max_results must be a positive integer")

        results: List[Dict] = []
        start_index = 1

        while len(results) < limit:
            remaining = limit - len(results)
            num = min(self.num_per_request, remaining, 10)
            data = self.search(query=query, num_results=num,
                               start_index=start_index)

            items = data.get("items", [])
            if not items:
                break

            results.extend(items[:remaining])

            fetched = len(items)
            start_index = start_index + fetched
            if fetched < num:
                break

        return results

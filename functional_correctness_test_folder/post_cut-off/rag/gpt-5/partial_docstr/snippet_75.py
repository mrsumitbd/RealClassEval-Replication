import requests


class GoogleCustomSearchAPI:
    """Google Custom Search API Client"""

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):
        """
        Initialize Google Custom Search API client
        Args:
            api_key: Google API key
            search_engine_id: Search engine ID (cx parameter)
            max_results: Maximum number of results to retrieve
            num_per_request: Number of results per API request
        """
        if not api_key:
            raise ValueError('api_key must be provided')
        if not search_engine_id:
            raise ValueError('search_engine_id must be provided')
        if max_results <= 0:
            raise ValueError('max_results must be a positive integer')
        if num_per_request <= 0:
            raise ValueError('num_per_request must be a positive integer')

        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = int(max_results)
        self.num_per_request = min(int(num_per_request), 10)
        self._endpoint = 'https://www.googleapis.com/customsearch/v1'
        self._session = requests.Session()
        self._timeout = 15

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
        if not isinstance(query, str) or not query.strip():
            raise ValueError('query must be a non-empty string')
        if start_index < 1:
            raise ValueError('start_index must be >= 1')

        num = self.num_per_request if num_results is None else int(num_results)
        if num <= 0:
            raise ValueError('num_results must be a positive integer')
        num = min(num, 10)

        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': num,
            'start': start_index,
        }

        resp = self._session.get(
            self._endpoint, params=params, timeout=self._timeout)
        resp.raise_for_status()
        return resp.json()

    def get_all_results(self, query: str, max_results: int | None = None) -> list[dict]:
        """
        Get all search results (with pagination)
        Args:
            query: Search query
            max_results: Maximum number of results (uses config default if None)
        Returns:
            List of all search results
        """
        limit = self.max_results if max_results is None else int(max_results)
        if limit <= 0:
            raise ValueError('max_results must be a positive integer')

        results: list[dict] = []
        start_index = 1

        while len(results) < limit:
            to_get = min(self.num_per_request, limit - len(results))
            data = self.search(query, num_results=to_get,
                               start_index=start_index)
            items = data.get('items') or []
            if not items:
                break

            results.extend(items)

            next_start = None
            queries = data.get('queries') or {}
            next_pages = queries.get('nextPage') or []
            if next_pages:
                next_start = next_pages[0].get('startIndex')

            if isinstance(next_start, int) and next_start > start_index:
                start_index = next_start
            else:
                start_index += len(items)

        return results

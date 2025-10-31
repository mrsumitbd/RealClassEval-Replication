import requests
from typing import List, Dict, Optional, Any


class GoogleCustomSearchAPIError(Exception):
    pass


class GoogleCustomSearchAPI:
    '''Google Custom Search API Client'''

    BASE_URL = 'https://www.googleapis.com/customsearch/v1'
    MAX_RESULTS_LIMIT = 100
    MAX_NUM_PER_REQUEST = 10

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
            raise ValueError('api_key must be a non-empty string.')
        if not search_engine_id or not isinstance(search_engine_id, str):
            raise ValueError('search_engine_id must be a non-empty string.')

        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = self._sanitize_max_results(max_results)
        self.num_per_request = self._sanitize_num_per_request(num_per_request)
        self.timeout = 30

        self.session = requests.Session()
        self.session.params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
        }

    def _sanitize_num_per_request(self, value: int) -> int:
        try:
            v = int(value)
        except Exception as e:
            raise ValueError('num_per_request must be an integer.') from e
        if v < 1:
            v = 1
        if v > self.MAX_NUM_PER_REQUEST:
            v = self.MAX_NUM_PER_REQUEST
        return v

    def _sanitize_max_results(self, value: int) -> int:
        try:
            v = int(value)
        except Exception as e:
            raise ValueError('max_results must be an integer.') from e
        if v < 1:
            v = 1
        if v > self.MAX_RESULTS_LIMIT:
            v = self.MAX_RESULTS_LIMIT
        return v

    def _request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = self.session.get(
                self.BASE_URL, params=params, timeout=self.timeout)
        except requests.RequestException as e:
            raise GoogleCustomSearchAPIError(f'Network error: {e}') from e

        content_type = resp.headers.get('Content-Type', '')
        data: Dict[str, Any] = {}
        if 'application/json' in content_type.lower():
            try:
                data = resp.json()
            except ValueError:
                pass

        if resp.status_code != 200:
            error_message = 'HTTP error'
            if data.get('error'):
                err = data['error']
                if isinstance(err, dict):
                    message = err.get('message') or ''
                    code = err.get('code')
                    error_message = f'API error {code}: {message}' if code else f'API error: {message}'
            else:
                error_message = f'HTTP {resp.status_code}: {resp.text}'
            raise GoogleCustomSearchAPIError(error_message)

        if isinstance(data, dict) and data.get('error'):
            err = data['error']
            if isinstance(err, dict):
                message = err.get('message') or 'Unknown error'
                code = err.get('code')
                raise GoogleCustomSearchAPIError(
                    f'API error {code}: {message}' if code else f'API error: {message}')
            raise GoogleCustomSearchAPIError('Unknown API error')

        return data

    def search(self, query: str, num_results: int | None = None, start_index: int = 1) -> dict:
        '''
        Execute search request
        Args:
            query: Search query
            num_results: Number of results to return (uses config default if None)
            start_index: Starting index (default 1)
        Returns:
            Dictionary containing search results
        '''
        if not isinstance(query, str) or not query.strip():
            raise ValueError('query must be a non-empty string.')

        num = self.num_per_request if num_results is None else self._sanitize_num_per_request(
            num_results)

        try:
            start = int(start_index)
        except Exception as e:
            raise ValueError('start_index must be an integer.') from e
        if start < 1:
            start = 1
        if start > self.MAX_RESULTS_LIMIT:
            # Google API does not allow start index beyond accessible range
            return {'items': []}

        params = {
            'q': query,
            'num': num,
            'start': start,
        }
        return self._request(params)

    def get_all_results(self, query: str, max_results: int | None = None) -> list[dict]:
        '''
        Get all search results (with pagination)
        Args:
            query: Search query
            max_results: Maximum number of results (uses config default if None)
        Returns:
            List of all search results
        '''
        target_max = self.max_results if max_results is None else self._sanitize_max_results(
            max_results)
        if target_max <= 0:
            return []

        results: List[Dict[str, Any]] = []
        start = 1

        while len(results) < target_max:
            remaining = target_max - len(results)
            page_size = min(self.num_per_request, remaining)
            data = self.search(query, num_results=page_size, start_index=start)

            items = data.get('items') or []
            if not items:
                break

            results.extend(items)

            next_start = None
            queries = data.get('queries', {})
            next_page = queries.get('nextPage')
            if isinstance(next_page, list) and next_page:
                next_start = next_page[0].get('startIndex')

            if next_start is None:
                start += len(items)
            else:
                try:
                    start = int(next_start)
                except Exception:
                    start += len(items)

            if start > self.MAX_RESULTS_LIMIT:
                break

            try:
                total_results_str = data.get(
                    'searchInformation', {}).get('totalResults')
                if total_results_str is not None:
                    total_results = int(total_results_str)
                    if len(results) >= total_results:
                        break
            except Exception:
                pass

        return results

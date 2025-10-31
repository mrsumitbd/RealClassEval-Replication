
import requests


class XinyuSearchAPI:
    '''Xinyu Search API Client'''

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        '''
        Initialize Xinyu Search API client
        Args:
            access_key: Xinyu API access key
            search_engine_id: Xinyu Search Engine ID
            max_results: Maximum number of results to retrieve
        '''
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        '''
        Query detailed search results with a custom request body.
        Args:
            body: Custom request body for the API call
            detail: Whether to include detailed results
        Returns:
            List of search results as dictionaries
        '''
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

        if detail:
            return data.get('items', [])
        else:
            return [{'title': item.get('title'), 'link': item.get('link')} for item in data.get('items', [])]

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        '''
        Perform a search query.
        Args:
            query: Search query string
            max_results: Maximum number of results to retrieve (overrides default)
        Returns:
            List of search results as dictionaries
        '''
        num_results = max_results if max_results is not None else self.max_results

        params = {
            'key': self.access_key,
            'cx': self.search_engine_id,
            'q': query,
            'num': num_results
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()

        return data.get('items', [])

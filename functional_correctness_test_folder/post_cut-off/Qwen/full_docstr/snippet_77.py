
class XinyuSearchAPI:
    '''Xinyu Search API Client'''

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        '''
        Initialize Xinyu Search API client
        Args:
            access_key: Xinyu API access key
            max_results: Maximum number of results to retrieve
        '''
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        '''
        Query Xinyu search API for detailed results
        Args:
            body: Search parameters
            detail: Whether to get detailed results
        Returns:
            List of search results
        '''
        # Simulate API call and response
        if body is None:
            body = {}
        results = [
            {"id": 1, "title": "Result 1", "content": "Content of result 1"},
            {"id": 2, "title": "Result 2", "content": "Content of result 2"},
        ]
        if not detail:
            return [{"id": result["id"], "title": result["title"]} for result in results]
        return results

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        '''
        Execute search request
        Args:
            query: Search query
            max_results: Maximum number of results to return
        Returns:
            List of search results
        '''
        # Simulate API call and response
        if max_results is None:
            max_results = self.max_results
        results = [
            {"id": 1, "title": "Result 1", "content": "Content of result 1"},
            {"id": 2, "title": "Result 2", "content": "Content of result 2"},
            {"id": 3, "title": "Result 3", "content": "Content of result 3"},
        ]
        return results[:max_results]

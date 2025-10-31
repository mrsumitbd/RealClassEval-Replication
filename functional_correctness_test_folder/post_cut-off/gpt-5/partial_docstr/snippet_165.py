from typing import List


class ToolHistory:

    def __init__(self):
        '''Initialize empty sets for tracking URLs and queries.'''
        self._visited_urls = set()
        self._searched_queries = set()

    def add_visited_urls(self, urls: List[str]) -> None:
        if not urls:
            return
        for url in urls:
            if isinstance(url, str) and url:
                self._visited_urls.add(url)

    def add_searched_queries(self, queries: List[str]) -> None:
        '''Add search queries to the set of searched queries.
        Args:
            queries: List of search queries to add
        '''
        if not queries:
            return
        for query in queries:
            if isinstance(query, str) and query:
                self._searched_queries.add(query)

    def get_visited_urls(self) -> List[str]:
        '''Get list of all visited URLs.
        Returns:
            List of visited URLs
        '''
        return sorted(self._visited_urls)

    def get_searched_queries(self) -> List[str]:
        return sorted(self._searched_queries)

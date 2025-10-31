
from typing import List


class ToolHistory:

    def __init__(self):
        '''Initialize empty sets for tracking URLs and queries.'''
        self.visited_urls = set()
        self.searched_queries = set()

    def add_visited_urls(self, urls: List[str]) -> None:
        '''Add URLs to the set of visited URLs.
        Args:
            urls: List of URLs to add
        '''
        self.visited_urls.update(urls)

    def add_searched_queries(self, queries: List[str]) -> None:
        '''Add search queries to the set of searched queries.
        Args:
            queries: List of search queries to add
        '''
        self.searched_queries.update(queries)

    def get_visited_urls(self) -> List[str]:
        '''Get list of all visited URLs.
        Returns:
            List of visited URLs
        '''
        return list(self.visited_urls)

    def get_searched_queries(self) -> List[str]:
        '''Get list of all searched queries.
        Returns:
            List of searched queries
        '''
        return list(self.searched_queries)

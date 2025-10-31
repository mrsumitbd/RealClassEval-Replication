
from typing import List


class ToolHistory:
    def __init__(self):
        self._visited_urls: List[str] = []
        self._searched_queries: List[str] = []

    def add_visited_urls(self, urls: List[str]) -> None:
        """Add a list of visited URLs to the history."""
        self._visited_urls.extend(urls)

    def add_searched_queries(self, queries: List[str]) -> None:
        """Add a list of searched queries to the history."""
        self._searched_queries.extend(queries)

    def get_visited_urls(self) -> List[str]:
        """Return the list of visited URLs."""
        return list(self._visited_urls)

    def get_searched_queries(self) -> List[str]:
        """Return the list of searched queries."""
        return list(self._searched_queries)

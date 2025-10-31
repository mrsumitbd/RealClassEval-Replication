
from typing import List


class ToolHistory:

    def __init__(self):
        self._visited_urls = []
        self._searched_queries = []

    def add_visited_urls(self, urls: List[str]) -> None:
        self._visited_urls.extend(urls)

    def add_searched_queries(self, queries: List[str]) -> None:
        self._searched_queries.extend(queries)

    def get_visited_urls(self) -> List[str]:
        return list(self._visited_urls)

    def get_searched_queries(self) -> List[str]:
        return list(self._searched_queries)

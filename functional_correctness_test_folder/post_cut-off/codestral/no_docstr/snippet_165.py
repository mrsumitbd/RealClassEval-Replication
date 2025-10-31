
from typing import List


class ToolHistory:

    def __init__(self):
        self.visited_urls = []
        self.searched_queries = []

    def add_visited_urls(self, urls: List[str]) -> None:
        self.visited_urls.extend(urls)

    def add_searched_queries(self, queries: List[str]) -> None:
        self.searched_queries.extend(queries)

    def get_visited_urls(self) -> List[str]:
        return self.visited_urls

    def get_searched_queries(self) -> List[str]:
        return self.searched_queries

from typing import List


class ToolHistory:

    def __init__(self):
        self._visited_urls: List[str] = []
        self._searched_queries: List[str] = []

    def add_visited_urls(self, urls: List[str]) -> None:
        if urls is None:
            return
        if not isinstance(urls, list):
            raise TypeError("urls must be a list of strings")
        for url in urls:
            if not isinstance(url, str):
                raise TypeError("each url must be a string")
        self._visited_urls.extend(urls)

    def add_searched_queries(self, queries: List[str]) -> None:
        if queries is None:
            return
        if not isinstance(queries, list):
            raise TypeError("queries must be a list of strings")
        for q in queries:
            if not isinstance(q, str):
                raise TypeError("each query must be a string")
        self._searched_queries.extend(queries)

    def get_visited_urls(self) -> List[str]:
        return list(self._visited_urls)

    def get_searched_queries(self) -> List[str]:
        return list(self._searched_queries)

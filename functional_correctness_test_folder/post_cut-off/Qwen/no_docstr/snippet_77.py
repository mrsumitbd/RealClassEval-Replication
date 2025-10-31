
class XinyuSearchAPI:

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        # Simulated response for demonstration purposes
        if body is None:
            body = {}
        response = [
            {"id": 1, "title": "Example Title 1", "content": "Example content 1"},
            {"id": 2, "title": "Example Title 2", "content": "Example content 2"}
        ]
        if not detail:
            return [{"id": item["id"]} for item in response]
        return response

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        # Simulated search response for demonstration purposes
        if max_results is None:
            max_results = self.max_results
        response = [
            {"id": 1, "title": "Search Result 1", "content": "Relevant content 1"},
            {"id": 2, "title": "Search Result 2", "content": "Relevant content 2"},
            {"id": 3, "title": "Search Result 3", "content": "Relevant content 3"}
        ]
        return response[:max_results]

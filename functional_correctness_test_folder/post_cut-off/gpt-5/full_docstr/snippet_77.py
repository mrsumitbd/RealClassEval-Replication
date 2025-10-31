class XinyuSearchAPI:
    '''Xinyu Search API Client'''

    DEFAULT_BASE_URL = "https://api.xinyu.ai/v1/search"

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        '''
        Initialize Xinyu Search API client
        Args:
            access_key: Xinyu API access key
            max_results: Maximum number of results to retrieve
        '''
        if not isinstance(access_key, str) or not access_key.strip():
            raise ValueError("access_key must be a non-empty string")
        if not isinstance(search_engine_id, str) or not search_engine_id.strip():
            raise ValueError("search_engine_id must be a non-empty string")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer")

        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.base_url = self.DEFAULT_BASE_URL
        self._timeout = 15

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        '''
        Query Xinyu search API for detailed results
        Args:
            body: Search parameters
            detail: Whether to get detailed results
        Returns:
            List of search results
        '''
        payload: dict = {
            "engine_id": self.search_engine_id,
            "detail": bool(detail),
            "size": self.max_results,
        }
        if body:
            if not isinstance(body, dict):
                raise TypeError("body must be a dict if provided")
            payload.update(body)

        return self._post_and_extract(payload)

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        '''
        Execute search request
        Args:
            query: Search query
            max_results: Maximum number of results to return
        Returns:
            List of search results
        '''
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        size = self.max_results if max_results is None else max_results
        if not isinstance(size, int) or size <= 0:
            raise ValueError(
                "max_results must be a positive integer when provided")

        payload = {
            "engine_id": self.search_engine_id,
            "q": query,
            "size": size,
            "detail": False,
        }
        return self._post_and_extract(payload)

    # Internal helpers

    def _post_and_extract(self, payload: dict) -> list[dict]:
        import json
        from urllib import request, error

        req = request.Request(
            self.base_url,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.access_key}",
                "User-Agent": "xinyu-search-python/1.0",
            },
            data=json.dumps(payload).encode("utf-8"),
        )

        try:
            with request.urlopen(req, timeout=self._timeout) as resp:
                raw = resp.read()
                try:
                    data = json.loads(raw.decode("utf-8"))
                except Exception as e:
                    raise RuntimeError(
                        f"Failed to parse response JSON: {e}") from e
        except error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(
                f"HTTP {e.code} error from Xinyu Search API: {detail}") from e
        except error.URLError as e:
            raise RuntimeError(
                f"Network error connecting to Xinyu Search API: {e}") from e

        # Normalize result extraction from common shapes
        results = []
        if isinstance(data, dict):
            if "results" in data and isinstance(data["results"], list):
                results = data["results"]
            elif "data" in data:
                if isinstance(data["data"], list):
                    results = data["data"]
                elif isinstance(data["data"], dict) and isinstance(data["data"].get("results"), list):
                    results = data["data"]["results"]
        if not isinstance(results, list):
            results = []

        # Ensure items are dicts
        results = [r for r in results if isinstance(r, dict)]
        return results

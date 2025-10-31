class GoogleCustomSearchAPI:
    '''Google Custom Search API Client'''

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("api_key must be a non-empty string")
        if not search_engine_id or not isinstance(search_engine_id, str):
            raise ValueError("search_engine_id must be a non-empty string")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer")
        if not isinstance(num_per_request, int) or num_per_request <= 0:
            raise ValueError("num_per_request must be a positive integer")

        # Google CSE limits: num per request is 1..10, total results capped at 100
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.num_per_request = max(1, min(10, num_per_request))
        self.endpoint = "https://www.googleapis.com/customsearch/v1"
        self._headers = {
            "User-Agent": "GoogleCustomSearchAPI/1.0 (+https://developers.google.com/custom-search/)",
            "Accept": "application/json",
        }

    def _request(self, params: dict, timeout: float = 10.0, retries: int = 3, backoff: float = 0.8) -> dict:
        import urllib.parse
        import urllib.request
        import urllib.error
        import json
        import time

        query = urllib.parse.urlencode(params, doseq=True, safe=":+")
        url = f"{self.endpoint}?{query}"

        last_exc = None
        for attempt in range(retries + 1):
            try:
                req = urllib.request.Request(
                    url, headers=self._headers, method="GET")
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    charset = resp.headers.get_content_charset() or "utf-8"
                    data = resp.read().decode(charset, errors="replace")
                    return json.loads(data) if data else {}
            except urllib.error.HTTPError as e:
                # Retry on rate limit and transient server errors
                if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                    sleep_for = backoff * (2 ** attempt)
                    time.sleep(sleep_for)
                    last_exc = e
                    continue
                # Try to extract JSON body if present
                try:
                    body = e.read()
                    if body:
                        import json as _json
                        parsed = _json.loads(
                            body.decode("utf-8", errors="replace"))
                        raise RuntimeError(
                            f"HTTPError {e.code}: {parsed}") from None
                except Exception:
                    pass
                raise
            except (urllib.error.URLError, TimeoutError) as e:
                if attempt < retries:
                    sleep_for = backoff * (2 ** attempt)
                    time.sleep(sleep_for)
                    last_exc = e
                    continue
                raise
        if last_exc:
            raise last_exc
        return {}

    def search(self, query: str, num_results: int | None = None, start_index: int = 1) -> dict:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if not isinstance(start_index, int) or start_index < 1:
            raise ValueError("start_index must be an integer >= 1")

        # Google CSE enforces 1..10 per request
        if num_results is None:
            num = self.num_per_request
        else:
            if not isinstance(num_results, int) or num_results <= 0:
                raise ValueError("num_results must be a positive integer")
            num = max(1, min(10, num_results))

        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": num,
            "start": start_index,
        }
        return self._request(params)

    def get_all_results(self, query: str, max_results: int | None = None) -> list[dict]:
        # Google caps total accessible results to ~100 per query
        if max_results is None:
            remaining = self.max_results
        else:
            if not isinstance(max_results, int) or max_results <= 0:
                raise ValueError("max_results must be a positive integer")
            remaining = max_results
        remaining = min(remaining, 100)

        all_items: list[dict] = []
        start_index = 1

        while remaining > 0:
            batch_size = min(self.num_per_request, remaining)
            resp = self.search(
                query=query, num_results=batch_size, start_index=start_index)
            items = resp.get("items") or []
            if not items:
                break
            all_items.extend(items[:batch_size])

            fetched = len(items)
            remaining -= fetched
            # Next start index can be obtained from queries.nextPage[0].startIndex if present
            next_info = None
            queries = resp.get("queries") or {}
            next_pages = queries.get("nextPage") or []
            if next_pages:
                next_info = next_pages[0]
            if next_info and isinstance(next_info, dict) and "startIndex" in next_info:
                start_index = int(next_info["startIndex"])
            else:
                # Fallback to increment by fetched count
                start_index += fetched

            if fetched == 0:
                break

        return all_items

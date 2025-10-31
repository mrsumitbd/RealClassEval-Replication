class BochaAISearchAPI:
    '''BochaAI Search API Client'''

    _BASE_URL = "https://api.bocha.ai/search"
    _FRESHNESS_OPTIONS = {"noLimit", "hour", "day", "week", "month"}

    def __init__(self, api_key: str, max_results: int = 20):
        '''
        Initialize BochaAI Search API client.
        Args:
            api_key: BochaAI API key
            max_results: Maximum number of search results to retrieve
        '''
        if not api_key or not isinstance(api_key, str):
            raise ValueError("api_key must be a non-empty string")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer")
        self.api_key = api_key
        self.max_results = max_results

    def search_web(self, query: str, summary: bool = True, freshness: str = 'noLimit') -> list[dict]:
        '''
        Perform a Web Search (equivalent to the first curl).
        Args:
            query: Search query string
            summary: Whether to include summary in the results
            freshness: Freshness filter (e.g. 'noLimit', 'day', 'week')
        Returns:
            A list of search result dicts
        '''
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")
        if freshness not in self._FRESHNESS_OPTIONS:
            raise ValueError(
                f"freshness must be one of {sorted(self._FRESHNESS_OPTIONS)}")

        body = {
            "query": query,
            "summary": bool(summary),
            "freshness": freshness,
            "maxResults": self.max_results,
        }
        url = f"{self._BASE_URL}/web"
        return self._post(url, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness: str = 'noLimit') -> list[dict]:
        '''
        Perform an AI Search (equivalent to the second curl).
        Args:
            query: Search query string
            answer: Whether BochaAI should generate an answer
            stream: Whether to use streaming response
            freshness: Freshness filter (e.g. 'noLimit', 'day', 'week')
        Returns:
            A list of search result dicts
        '''
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")
        if freshness not in self._FRESHNESS_OPTIONS:
            raise ValueError(
                f"freshness must be one of {sorted(self._FRESHNESS_OPTIONS)}")

        body = {
            "query": query,
            "answer": bool(answer),
            "stream": bool(stream),
            "freshness": freshness,
            "maxResults": self.max_results,
        }
        url = f"{self._BASE_URL}/ai"
        return self._post(url, body)

    def _post(self, url: str, body: dict) -> list[dict]:
        '''Send POST request and parse BochaAI search results.'''
        import json
        import requests

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "BochaAISearchAPI/1.0",
        }

        try:
            resp = requests.post(url, headers=headers,
                                 data=json.dumps(body), timeout=30)
        except requests.RequestException as e:
            raise RuntimeError(
                f"Network error while calling BochaAI: {e}") from e

        if resp.status_code == 401:
            raise PermissionError("Unauthorized: invalid API key")
        if resp.status_code == 403:
            raise PermissionError("Forbidden: insufficient permissions")
        if resp.status_code == 404:
            raise RuntimeError("Endpoint not found")
        if resp.status_code >= 400:
            # Try to parse error message from JSON
            try:
                err = resp.json()
                msg = err.get("error") or err.get("message") or str(err)
            except Exception:
                msg = resp.text or f"HTTP {resp.status_code}"
            raise RuntimeError(f"BochaAI API error: {msg}")

        try:
            data = resp.json()
        except ValueError:
            raise RuntimeError("Invalid JSON response from BochaAI")

        # Normalize to a list[dict]
        # Common patterns: {"results": [...]}, {"data": [...]}, or a bare list
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict)]

        if isinstance(data, dict):
            for key in ("results", "data", "items"):
                if key in data and isinstance(data[key], list):
                    return [x for x in data[key] if isinstance(x, dict)]
            # If response is a dict but doesn't contain a list, wrap it
            return [data]

        # Fallback: wrap unknown types
        return [{"value": data}]

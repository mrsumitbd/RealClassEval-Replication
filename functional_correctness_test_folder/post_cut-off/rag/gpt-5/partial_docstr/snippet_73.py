import json
from typing import Any, Dict, List
import requests


class BochaAISearchAPI:
    """BochaAI Search API Client"""

    WEB_SEARCH_URL = "https://api.bocha.ai/search/web"
    AI_SEARCH_URL = "https://api.bocha.ai/search/ai"

    def __init__(self, api_key: str, max_results: int = 20):
        """
        Initialize BochaAI Search API client.
        Args:
            api_key: BochaAI API key
            max_results: Maximum number of search results to retrieve
        """
        self.api_key = api_key
        self.max_results = max_results
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "BochaAISearchAPI/1.0",
            }
        )
        self.timeout = 30

    def search_web(self, query: str, summary: bool = True, freshness: str = "noLimit") -> list[dict]:
        """
        Perform a Web Search (equivalent to the first curl).
        Args:
            query: Search query string
            summary: Whether to include summary in the results
            freshness: Freshness filter (e.g. 'noLimit', 'day', 'week')
        Returns:
            A list of search result dicts
        """
        body: Dict[str, Any] = {
            "query": query,
            "summary": summary,
            "freshness": freshness,
            "maxResults": self.max_results,
        }
        return self._post(self.WEB_SEARCH_URL, body)

    def search_ai(
        self, query: str, answer: bool = False, stream: bool = False, freshness: str = "noLimit"
    ) -> list[dict]:
        """
        Perform an AI Search (equivalent to the second curl).
        Args:
            query: Search query string
            answer: Whether BochaAI should generate an answer
            stream: Whether to use streaming response
            freshness: Freshness filter (e.g. 'noLimit', 'day', 'week')
        Returns:
            A list of search result dicts
        """
        body: Dict[str, Any] = {
            "query": query,
            "answer": answer,
            "stream": stream,
            "freshness": freshness,
            "maxResults": self.max_results,
        }

        if stream:
            # Adjust headers for SSE
            headers = self.session.headers.copy()
            headers["Accept"] = "text/event-stream"
            try:
                resp = self.session.post(
                    self.AI_SEARCH_URL, data=json.dumps(body), headers=headers, timeout=self.timeout, stream=True
                )
                resp.raise_for_status()
            except requests.RequestException as e:
                raise RuntimeError(f"BochaAI request failed: {e}") from e

            results: List[Dict[str, Any]] = []
            try:
                for line in resp.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    # Basic SSE parsing
                    if line.startswith("data:"):
                        data_str = line[len("data:"):].strip()
                        if data_str in ("[DONE]", ""):
                            continue
                        try:
                            payload = json.loads(data_str)
                        except json.JSONDecodeError:
                            continue
                        results.extend(self._normalize_results(payload))
            finally:
                resp.close()
            return results

        return self._post(self.AI_SEARCH_URL, body)

    def _post(self, url: str, body: dict) -> list[dict]:
        """Send POST request and parse BochaAI search results."""
        try:
            resp = self.session.post(
                url, data=json.dumps(body), timeout=self.timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"BochaAI request failed: {e}") from e

        try:
            payload = resp.json()
        except ValueError as e:
            raise RuntimeError(f"Invalid JSON in BochaAI response: {e}") from e

        return self._normalize_results(payload)

    @staticmethod
    def _normalize_results(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Normalize various possible BochaAI-like response shapes into a list of result dicts.
        This is defensive to accommodate minor API variations.
        """
        # Common patterns
        for key in ("results", "data", "items", "value"):
            if isinstance(payload, dict) and key in payload and isinstance(payload[key], list):
                return [item for item in payload[key] if isinstance(item, dict)]

        # Nested patterns (e.g., webPages.value)
        if isinstance(payload, dict) and "webPages" in payload:
            wp = payload.get("webPages") or {}
            if isinstance(wp, dict) and isinstance(wp.get("value"), list):
                return [item for item in wp["value"] if isinstance(item, dict)]

        # Single result object
        if isinstance(payload, dict) and "result" in payload and isinstance(payload["result"], dict):
            return [payload["result"]]

        # If none of the above, and payload itself looks like a result dict
        if isinstance(payload, dict):
            return [payload]

        # Fallback: empty
        return []

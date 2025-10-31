import os
import json
from typing import Any, Dict, List, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BochaAISearchAPI:
    '''BochaAI Search API Client'''

    DEFAULT_BASE_URL = "https://api.bocha.ai/v1"
    ENV_BASE_URL = "BOCHAAI_BASE_URL"

    def __init__(self, api_key: str, max_results: int = 20):
        '''
        Initialize BochaAI Search API client.
        Args:
            api_key: BochaAI API key
            max_results: Maximum number of search results to retrieve
        '''
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("api_key must be a non-empty string.")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer.")

        self.api_key = api_key.strip()
        self.max_results = max_results
        self.base_url = os.getenv(
            self.ENV_BASE_URL, self.DEFAULT_BASE_URL).rstrip("/")
        self._session = self._build_session()

    def search_web(self, query: str, summary: bool = True, freshness: str = 'noLimit') -> list[dict]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string.")
        if freshness not in ('noLimit', 'day', 'week', 'month', 'year'):
            raise ValueError(
                "freshness must be one of: 'noLimit', 'day', 'week', 'month', 'year'.")
        url = f"{self.base_url}/search/web"
        body = {
            "query": query.strip(),
            "maxResults": self.max_results,
            "summary": bool(summary),
            "freshness": freshness,
        }
        return self._post(url, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness: str = 'noLimit') -> list[dict]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string.")
        if freshness not in ('noLimit', 'day', 'week', 'month', 'year'):
            raise ValueError(
                "freshness must be one of: 'noLimit', 'day', 'week', 'month', 'year'.")
        url = f"{self.base_url}/search/ai"
        body = {
            "query": query.strip(),
            "maxResults": self.max_results,
            "answer": bool(answer),
            "stream": bool(stream),
            "freshness": freshness,
        }
        return self._post(url, body)

    def _post(self, url: str, body: dict) -> list[dict]:
        '''Send POST request and parse BochaAI search results.'''
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "BochaAISearchAPI/1.0",
        }
        try:
            resp = self._session.post(
                url, headers=headers, json=body, timeout=(5, 30))
        except requests.RequestException as exc:
            raise RuntimeError(
                f"Failed to connect to BochaAI API: {exc}") from exc

        if not (200 <= resp.status_code < 300):
            content = None
            try:
                content = resp.json()
            except Exception:
                content = resp.text
            raise requests.HTTPError(
                f"BochaAI API error {resp.status_code}: {content}",
                response=resp,
            )

        # Try JSON first
        try:
            payload = resp.json()
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Invalid JSON response from BochaAI API.") from exc

        results = self._normalize_results(payload)
        return results

    @staticmethod
    def _normalize_results(payload: Any) -> List[Dict[str, Any]]:
        if payload is None:
            return []
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        if isinstance(payload, dict):
            for key in ("results", "data", "items"):
                val = payload.get(key)
                if isinstance(val, list):
                    return [item for item in val if isinstance(item, dict)]
            # If the dict itself looks like a single result, wrap it
            return [payload]
        return []

    @staticmethod
    def _build_session() -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=0.3,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["POST"]),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(
            max_retries=retry, pool_connections=10, pool_maxsize=10)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

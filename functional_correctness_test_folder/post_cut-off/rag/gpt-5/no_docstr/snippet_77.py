import os
import json
from typing import Any, Dict, List, Optional

try:
    import requests
except Exception:  # pragma: no cover
    requests = None


class XinyuSearchAPIError(Exception):
    pass


class XinyuSearchAPI:
    """Xinyu Search API Client"""

    DEFAULT_BASE_URL = "https://api.xinyu.ai/v1/search"
    DEFAULT_TIMEOUT = 15

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        """
        Initialize Xinyu Search API client
        Args:
            access_key: Xinyu API access key
            max_results: Maximum number of results to retrieve
        """
        if not access_key or not isinstance(access_key, str):
            raise ValueError("access_key must be a non-empty string")
        if not search_engine_id or not isinstance(search_engine_id, str):
            raise ValueError("search_engine_id must be a non-empty string")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer")

        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results

        self.base_url = os.getenv(
            "XINYU_SEARCH_API_URL", self.DEFAULT_BASE_URL).rstrip("/")
        timeout_env = os.getenv("XINYU_SEARCH_TIMEOUT")
        self.timeout = self.DEFAULT_TIMEOUT if timeout_env is None else max(
            1, int(timeout_env))

        if requests is None:
            raise RuntimeError(
                "The 'requests' library is required to use XinyuSearchAPI")

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self.access_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _build_url(self, path: str) -> str:
        path = path.lstrip("/")
        return f"{self.base_url}/{path}"

    def _parse_results(self, data: Any) -> List[Dict]:
        if data is None:
            return []
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict)]
        if isinstance(data, dict):
            for key in ("results", "items", "data"):
                if key in data and isinstance(data[key], list):
                    return [x for x in data[key] if isinstance(x, dict)]
        return []

    def _handle_response(self, resp) -> List[Dict]:
        try:
            resp.raise_for_status()
        except Exception as e:
            # Try to extract API error if available
            err_msg = None
            try:
                payload = resp.json()
                if isinstance(payload, dict):
                    err_msg = payload.get("error") or payload.get(
                        "message") or payload.get("detail")
            except Exception:
                pass
            if err_msg:
                raise XinyuSearchAPIError(
                    f"HTTP {resp.status_code}: {err_msg}") from e
            raise XinyuSearchAPIError(
                f"HTTP {resp.status_code}: {resp.text}") from e
        try:
            payload = resp.json()
        except Exception as e:
            raise XinyuSearchAPIError("Failed to parse JSON response") from e
        return self._parse_results(payload)

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        """
        Query Xinyu search API for detailed results
        Args:
            body: Search parameters
            detail: Whether to get detailed results
        Returns:
            List of search results
        """
        payload: Dict[str, Any] = {}
        if body:
            if not isinstance(body, dict):
                raise ValueError("body must be a dict or None")
            payload.update(body)

        payload.setdefault("search_engine_id", self.search_engine_id)
        payload.setdefault("engine_id", self.search_engine_id)
        payload["detail"] = bool(detail)

        # Default limit if not provided
        if "limit" not in payload and "max_results" not in payload:
            payload["limit"] = self.max_results

        url = self._build_url("query")
        resp = self._session.post(
            url, data=json.dumps(payload), timeout=self.timeout)
        return self._handle_response(resp)

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        """
        Execute search request
        Args:
            query: Search query
            max_results: Maximum number of results to return
        Returns:
            List of search results
        """
        if not isinstance(query, str) or not query.strip():
            return []
        limit = self.max_results if max_results is None else max_results
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError(
                "max_results must be a positive integer when provided")
        body = {
            "q": query,
            "query": query,
            "limit": limit,
            "search_engine_id": self.search_engine_id,
        }
        return self.query_detail(body=body, detail=False)

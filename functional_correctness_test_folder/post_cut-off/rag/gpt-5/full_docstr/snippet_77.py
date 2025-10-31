import json
import os
from typing import Any

from urllib import request, error


class XinyuSearchAPI:
    '''Xinyu Search API Client'''

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

        # Allow overriding base URL via environment for testing
        self.base_url = os.environ.get(
            'XINYU_SEARCH_BASE_URL', 'https://api.xinyu-search.com/v1/search')
        self.timeout = float(os.environ.get('XINYU_SEARCH_TIMEOUT', '15'))

        self._default_headers = {
            'Authorization': f'Bearer {self.access_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        '''
        Query Xinyu search API for detailed results
        Args:
            body: Search parameters
            detail: Whether to get detailed results
        Returns:
            List of search results
        '''
        payload: dict[str, Any] = dict(body or {})
        payload.setdefault('engine_id', self.search_engine_id)

        # Normalize limit/max_results parameter
        limit = payload.pop('max_results', None)
        if limit is None:
            limit = payload.get('limit', None)
        if limit is None:
            limit = self.max_results

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            raise ValueError("max_results/limit must be an integer")

        if limit <= 0:
            raise ValueError("max_results/limit must be a positive integer")

        payload['limit'] = limit
        payload['detail'] = bool(detail)

        resp = self._post_json(self.base_url, payload)
        results = self._extract_results(resp)

        # Ensure results are list[dict]
        normalized: list[dict] = []
        for item in results:
            if isinstance(item, dict):
                normalized.append(item)
            else:
                normalized.append({'value': item})
        return normalized

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

        limit = max_results if max_results is not None else self.max_results
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            raise ValueError("max_results must be an integer")
        if limit <= 0:
            raise ValueError("max_results must be a positive integer")

        body = {
            'query': query,
            'engine_id': self.search_engine_id,
            'limit': limit,
        }
        return self.query_detail(body=body, detail=False)

    def _post_json(self, url: str, payload: dict) -> dict:
        data = json.dumps(payload).encode('utf-8')
        req = request.Request(
            url, data=data, headers=self._default_headers, method='POST')
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                charset = resp.headers.get_content_charset() or 'utf-8'
                content = resp.read().decode(charset)
                if not content:
                    return {}
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    raise RuntimeError(f"Invalid JSON response: {e}") from e
        except error.HTTPError as e:
            try:
                err_body = e.read().decode('utf-8', errors='replace')
            except Exception:
                err_body = ''
            raise RuntimeError(
                f"HTTP {e.code} error from Xinyu Search API: {err_body or e.reason}") from e
        except error.URLError as e:
            raise RuntimeError(
                f"Failed to reach Xinyu Search API: {e.reason}") from e

    def _extract_results(self, resp: dict | list | None) -> list:
        if resp is None:
            return []
        if isinstance(resp, list):
            return resp
        if isinstance(resp, dict):
            for key in ('results', 'data', 'items'):
                val = resp.get(key)
                if isinstance(val, list):
                    return val
            # If response itself is a single result, wrap it
            return [resp]
        # Unknown shape, wrap as single item
        return [resp]

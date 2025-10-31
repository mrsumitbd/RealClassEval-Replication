import json
from typing import Any, Iterable, List, Dict, Optional

import requests


class BochaAISearchAPI:
    def __init__(self, api_key: str, max_results: int = 20):
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("api_key must be a non-empty string")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer")

        self.api_key = api_key.strip()
        self.max_results = max_results
        self.base_url = "https://api.bocha.ai"
        self.timeout = 30

    def search_web(self, query: str, summary: bool = True, freshness: str = "noLimit") -> list[dict]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        url = f"{self.base_url}/v1/search/web"
        body = {
            "query": query.strip(),
            "topK": self.max_results,
            "summary": bool(summary),
            "freshness": freshness,
        }
        return self._post(url, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness: str = "noLimit") -> list[dict]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")

        url = f"{self.base_url}/v1/search/ai"
        body = {
            "query": query.strip(),
            "topK": self.max_results,
            "answer": bool(answer),
            "stream": bool(stream),
            "freshness": freshness,
        }

        if not stream:
            return self._post(url, body)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

        results: List[Dict[str, Any]] = []
        with requests.post(url, headers=headers, json=body, timeout=self.timeout, stream=True) as resp:
            if resp.status_code >= 400:
                raise RuntimeError(f"HTTP {resp.status_code}: {resp.text}")

            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                chunk = line.strip()
                if chunk.lower().startswith("data:"):
                    chunk = chunk[5:].strip()
                try:
                    parsed = json.loads(chunk)
                except json.JSONDecodeError:
                    continue
                normalized = self._normalize_to_list(parsed)
                if isinstance(normalized, list):
                    results.extend(normalized)
                elif isinstance(parsed, dict):
                    results.append(parsed)
        return results

    def _post(self, url: str, body: dict) -> list[dict]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        resp = requests.post(url, headers=headers,
                             json=body, timeout=self.timeout)
        if resp.status_code == 204:
            return []
        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text}")

        if not resp.content:
            return []

        ct = resp.headers.get("Content-Type", "")
        if "application/json" in ct or resp.text.strip().startswith(("{", "[")):
            data = resp.json()
        else:
            raise RuntimeError("Unexpected content type from server")

        normalized = self._normalize_to_list(data)
        if isinstance(normalized, list):
            return normalized
        if isinstance(data, dict):
            return [data]
        return []

    def _normalize_to_list(self, data: Any) -> Optional[List[Dict[str, Any]]]:
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict)]
        if isinstance(data, dict):
            keys_in_order: Iterable[str] = (
                "results",
                "data",
                "documents",
                "items",
                "hits",
                "choices",
                "answers",
            )
            for k in keys_in_order:
                v = data.get(k)
                if isinstance(v, list):
                    return [d for d in v if isinstance(d, dict)]
        return None

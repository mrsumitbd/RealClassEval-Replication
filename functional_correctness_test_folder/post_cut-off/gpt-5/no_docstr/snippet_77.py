import requests
from typing import Any, Dict, List, Optional


class XinyuSearchAPI:
    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, access_key: str, search_engine_id: str, max_results: int = 20):
        if not isinstance(access_key, str) or not access_key.strip():
            raise ValueError("access_key must be a non-empty string")
        if not isinstance(search_engine_id, str) or not search_engine_id.strip():
            raise ValueError("search_engine_id must be a non-empty string")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer")

        self.access_key = access_key
        self.search_engine_id = search_engine_id
        self.max_results = max_results
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = self.session.get(self.BASE_URL, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if "error" in data:
                # Google CSE style error format
                message = data.get("error", {}).get(
                    "message", "Unknown API error")
                raise RuntimeError(f"API error: {message}")
            return data
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP error during search request: {e}") from e
        except ValueError as e:
            # JSON decoding error
            raise RuntimeError(f"Invalid JSON response: {e}") from e

    @staticmethod
    def _normalize_item(item: Dict[str, Any], include_raw: bool) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet"),
            "displayLink": item.get("displayLink"),
            "mime": item.get("mime"),
        }
        pagemap = item.get("pagemap")
        if isinstance(pagemap, dict):
            # Include a few commonly useful fields if present
            if "metatags" in pagemap and isinstance(pagemap["metatags"], list) and pagemap["metatags"]:
                meta0 = pagemap["metatags"][0]
                if isinstance(meta0, dict):
                    out["og:title"] = meta0.get("og:title")
                    out["og:description"] = meta0.get("og:description")
                    out["og:url"] = meta0.get("og:url")
        if include_raw:
            out["raw"] = item
        return out

    def query_detail(self, body: dict | None = None, detail: bool = True) -> list[dict]:
        params: Dict[str, Any] = {
            "key": self.access_key,
            "cx": self.search_engine_id,
        }
        if body:
            if not isinstance(body, dict):
                raise ValueError("body must be a dict if provided")
            params.update(body)

        if "q" not in params or not str(params["q"]).strip():
            raise ValueError("body must include a non-empty 'q' parameter")

        # Enforce Google CSE 'num' limit per request (1..10)
        num = int(params.get("num", min(self.max_results, 10)))
        num = max(1, min(10, num))
        params["num"] = num

        data = self._request(params)
        items = data.get("items") or []
        if not isinstance(items, list):
            return []

        return [self._normalize_item(it, include_raw=detail) for it in items if isinstance(it, dict)]

    def search(self, query: str, max_results: int | None = None) -> list[dict]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        total_wanted = max_results if (isinstance(
            max_results, int) and max_results > 0) else self.max_results

        results: List[Dict[str, Any]] = []
        start_index = 1  # Google CSE is 1-based
        while len(results) < total_wanted:
            remaining = total_wanted - len(results)
            # CSE allows up to 10 per request
            page_size = max(1, min(10, remaining))

            params = {
                "key": self.access_key,
                "cx": self.search_engine_id,
                "q": query,
                "start": start_index,
                "num": page_size,
            }

            data = self._request(params)
            items = data.get("items") or []
            if not items:
                break

            for it in items:
                if not isinstance(it, dict):
                    continue
                results.append(self._normalize_item(it, include_raw=False))
                if len(results) >= total_wanted:
                    break

            # Next page start index is current start + items returned
            start_index += len(items)

            # Stop if searchInfo totalResults indicates no more results
            try:
                total_results_str = data.get(
                    "searchInformation", {}).get("totalResults", "0")
                total_results_int = int(total_results_str)
                if start_index > total_results_int:
                    break
            except Exception:
                # If parsing fails, rely on items depletion
                pass

        return results[:total_wanted]

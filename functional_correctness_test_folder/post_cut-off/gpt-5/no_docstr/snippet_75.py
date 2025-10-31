import time
from typing import Optional
import requests


class GoogleCustomSearchAPI:
    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self, api_key: str, search_engine_id: str, max_results: int = 20, num_per_request: int = 10):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("api_key must be a non-empty string")
        if not search_engine_id or not isinstance(search_engine_id, str):
            raise ValueError("search_engine_id must be a non-empty string")

        self.api_key = api_key
        self.search_engine_id = search_engine_id

        self.max_results = max(1, int(max_results))
        # Google CSE limits num to 10
        self.num_per_request = max(1, min(10, int(num_per_request)))

        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def search(self, query: str, num_results: Optional[int] = None, start_index: int = 1) -> dict:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if start_index < 1 or start_index > 100:
            raise ValueError("start_index must be between 1 and 100")

        if num_results is None:
            num = self.num_per_request
        else:
            # API supports 1..10 per request
            num = max(1, min(10, int(num_results)))

        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "start": start_index,
            "num": num,
        }

        resp = self.session.get(self.BASE_URL, params=params, timeout=20)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            # Try to attach API error details if available
            try:
                err = resp.json()
                message = err.get("error", {}).get("message")
                if message:
                    raise requests.HTTPError(
                        f"{e} - {message}", response=resp) from None
            except Exception:
                pass
            raise

        data = resp.json()
        return data

    def get_all_results(self, query: str, max_results: Optional[int] = None) -> list[dict]:
        target = self.max_results if max_results is None else max(
            1, int(max_results))
        # CSE effectively caps retrievable results to 100
        target = min(target, 100)

        collected: list[dict] = []
        start_index = 1

        while len(collected) < target:
            remaining = target - len(collected)
            num = max(1, min(10, remaining))
            data = self.search(query=query, num_results=num,
                               start_index=start_index)

            items = data.get("items", [])
            if not items:
                break

            for item in items:
                collected.append(item)
                if len(collected) >= target:
                    break

            # Prefer nextPage startIndex if provided by API
            next_start = None
            try:
                queries = data.get("queries", {})
                next_pages = queries.get("nextPage", [])
                if next_pages:
                    next_start = int(next_pages[0].get(
                        "startIndex", 0)) or None
            except Exception:
                next_start = None

            if next_start is None:
                start_index = 1 + len(collected)
            else:
                start_index = next_start

            if start_index > 100:
                break

            time.sleep(0.1)

        return collected

from typing import Optional, Tuple, List, Dict, Any
import re
import requests
from urllib.parse import urljoin


class SimpleRegistryClient:
    def __init__(self, registry_url: Optional[str] = None):
        self.registry_url = registry_url.rstrip(
            "/") + "/" if registry_url else None
        self._timeout = (5, 15)

    def _ensure_url(self) -> str:
        if not self.registry_url:
            raise ValueError("registry_url is not set")
        return self.registry_url

    def _request(self, method: str, path: str, **kwargs) -> Any:
        base = self._ensure_url()
        url = urljoin(base, path.lstrip("/"))
        kwargs.setdefault("timeout", self._timeout)
        headers = kwargs.pop("headers", {})
        headers.setdefault("Accept", "application/json")
        if "json" in kwargs and "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
        resp = requests.request(method, url, headers=headers, **kwargs)
        resp.raise_for_status()
        if resp.status_code == 204:
            return None
        if "application/json" in resp.headers.get("Content-Type", ""):
            return resp.json()
        return resp.text

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        params: Dict[str, Any] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        data = self._request("GET", "/servers", params=params)

        if isinstance(data, list):
            return data, None

        items = []
        next_cursor: Optional[str] = None

        if isinstance(data, dict):
            for key in ("items", "results", "servers", "data"):
                if key in data and isinstance(data[key], list):
                    items = data[key]
                    break
            for nkey in ("next_cursor", "nextCursor", "cursor", "next"):
                val = data.get(nkey)
                if isinstance(val, str) and val:
                    next_cursor = val
                    break
                if isinstance(val, dict):
                    for k in ("cursor", "token", "id"):
                        if isinstance(val.get(k), str) and val.get(k):
                            next_cursor = val[k]
                            break
        return items, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        params = {"q": query}
        try:
            data = self._request("GET", "/servers/search", params=params)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code in (404, 405):
                data = self._request("GET", "/servers", params=params)
            else:
                raise

        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ("items", "results", "servers", "data"):
                if key in data and isinstance(data[key], list):
                    return data[key]
        return []

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        data = self._request("GET", f"/servers/{server_id}")
        if isinstance(data, dict):
            return data
        raise ValueError("Unexpected response format for server info")

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        results = self.search_servers(name)
        exact = None
        for item in results:
            n = item.get("name") or item.get("title") or item.get("id")
            if isinstance(n, str) and n.lower() == name.lower():
                exact = item
                break
        if exact:
            return exact
        for item in results:
            n = item.get("name") or item.get("title")
            if isinstance(n, str) and name.lower() in n.lower():
                return item
        return None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        if "@" in reference:
            left, right = reference.split("@", 1)
            right = right.strip()
            if right:
                try:
                    return self.get_server_info(right)
                except requests.HTTPError as e:
                    if e.response is not None and e.response.status_code == 404:
                        pass
                    else:
                        raise
            if left.strip():
                return self.get_server_by_name(left.strip())
            return None

        uuid_re = re.compile(
            r"^[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}$"
        )
        hex24_re = re.compile(r"^[0-9a-fA-F]{24}$")

        if uuid_re.match(reference) or hex24_re.match(reference):
            try:
                return self.get_server_info(reference)
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 404:
                    return None
                raise

        return self.get_server_by_name(reference)

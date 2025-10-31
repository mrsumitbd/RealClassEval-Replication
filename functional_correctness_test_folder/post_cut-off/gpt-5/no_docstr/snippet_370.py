from typing import Optional, Tuple, List, Dict, Any
import urllib.request
import urllib.parse
import json
import socket


class SimpleRegistryClient:
    def __init__(self, registry_url: Optional[str] = None):
        self.registry_url = (registry_url or "").rstrip("/")
        if not self.registry_url:
            self.registry_url = "http://localhost:8000"
        self._timeout = 15

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        params = {"limit": str(max(1, min(limit, 1000)))}
        if cursor:
            params["cursor"] = cursor
        data = self._request("servers", params=params)

        items, next_cursor = self._normalize_list_response(data)
        return items, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        # Try server-side search endpoints with common parameter names
        for path, param_key in (("servers/search", "q"), ("servers/search", "query"), ("servers", "search")):
            try:
                resp = self._request(path, params={param_key: query})
                items = self._normalize_items(resp)
                if items is not None:
                    return items
            except Exception:
                continue

        # Fallback to client-side filtering if server search unavailable
        results: List[Dict[str, Any]] = []
        cursor: Optional[str] = None
        while True:
            batch, cursor = self.list_servers(limit=200, cursor=cursor)
            for item in batch:
                if self._match_query(item, query):
                    results.append(item)
            if not cursor or not batch:
                break
        return results

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        if not server_id:
            raise ValueError("server_id must be non-empty")
        try:
            data = self._request(
                f"servers/{urllib.parse.quote(server_id, safe='')}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise KeyError(f"Server not found: {server_id}") from None
            raise
        if not isinstance(data, dict):
            raise RuntimeError("Unexpected response format for server info")
        return data

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        if not name:
            return None

        # Try dedicated endpoint if available
        for path in (f"servers/by-name/{urllib.parse.quote(name, safe='')}",):
            try:
                data = self._request(path)
                if isinstance(data, dict) and data:
                    return data
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    break
                continue
            except Exception:
                continue

        # Fallback: search and exact match by name or case-insensitive
        candidates = self.search_servers(name)
        exact = [s for s in candidates if self._get_name(s) == name]
        if exact:
            return exact[0]
        insensitive = [s for s in candidates if self._get_name(
            s).lower() == name.lower()]
        if insensitive:
            return insensitive[0]

        # Full scan as last resort
        cursor: Optional[str] = None
        while True:
            batch, cursor = self.list_servers(limit=200, cursor=cursor)
            for item in batch:
                if self._get_name(item) == name or self._get_name(item).lower() == name.lower():
                    return item
            if not cursor or not batch:
                break
        return None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        if not reference:
            return None

        # Try as ID
        try:
            return self.get_server_info(reference)
        except KeyError:
            pass
        except Exception:
            pass

        # Try as name
        by_name = self.get_server_by_name(reference)
        if by_name:
            return by_name

        # Try parsing "name@version" or "name:tag" style, match name first
        name_part = reference.split("@", 1)[0].split(":", 1)[0]
        if name_part and name_part != reference:
            by_name = self.get_server_by_name(name_part)
            if by_name:
                return by_name

        # Fallback: search and best-effort match
        results = self.search_servers(reference)
        if not results:
            return None
        # Prefer exact id match
        for s in results:
            sid = self._get_id(s)
            if sid and sid == reference:
                return s
        # Prefer exact name match
        for s in results:
            if self._get_name(s) == reference:
                return s
        # Return first candidate
        return results[0] if results else None

    # Internal helpers

    def _request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = self._build_url(path, params)
        req = urllib.request.Request(
            url, headers={"Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                content_type = resp.headers.get("Content-Type", "")
                raw = resp.read()
                if "application/json" in content_type or raw.startswith(b"{") or raw.startswith(b"["):
                    return json.loads(raw.decode("utf-8") or "null")
                # Fallback: try to parse JSON regardless
                try:
                    return json.loads(raw.decode("utf-8"))
                except Exception:
                    return raw.decode("utf-8", errors="replace")
        except urllib.error.HTTPError:
            raise
        except (urllib.error.URLError, socket.timeout) as e:
            raise ConnectionError(
                f"Failed to connect to registry at {url}: {e}") from None

    def _build_url(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        base = f"{self.registry_url}/{path.lstrip('/')}"
        if params:
            # Remove None values and encode
            qp = {k: v for k, v in params.items() if v is not None}
            return f"{base}?{urllib.parse.urlencode(qp)}" if qp else base
        return base

    def _normalize_list_response(self, data: Any) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        if isinstance(data, list):
            return self._ensure_dict_list(data), None
        if isinstance(data, dict):
            # Common keys for items
            for key in ("items", "servers", "data", "results"):
                if key in data and isinstance(data[key], list):
                    items = self._ensure_dict_list(data[key])
                    next_cursor = (
                        data.get("next_cursor")
                        or data.get("next")
                        or (data.get("cursor", {}).get("next") if isinstance(data.get("cursor"), dict) else None)
                    )
                    return items, next_cursor
            # Fallback: if dict looks like a single item
            if data:
                return [data], None
        return [], None

    def _normalize_items(self, data: Any) -> Optional[List[Dict[str, Any]]]:
        if isinstance(data, list):
            return self._ensure_dict_list(data)
        if isinstance(data, dict):
            for key in ("items", "servers", "data", "results"):
                if key in data and isinstance(data[key], list):
                    return self._ensure_dict_list(data[key])
            # Some search endpoints return {"matches":[...]}
            if "matches" in data and isinstance(data["matches"], list):
                return self._ensure_dict_list(data["matches"])
        return None

    def _ensure_dict_list(self, items: List[Any]) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for it in items:
            if isinstance(it, dict):
                out.append(it)
        return out

    def _match_query(self, item: Dict[str, Any], query: str) -> bool:
        q = query.lower()
        name = self._get_name(item).lower()
        sid = self._get_id(item).lower()
        if q in name or q in sid:
            return True
        # Search in description or tags if present
        desc = str(item.get("description") or "").lower()
        if q in desc:
            return True
        tags = item.get("tags")
        if isinstance(tags, list):
            for t in tags:
                if isinstance(t, str) and q in t.lower():
                    return True
        return False

    def _get_name(self, item: Dict[str, Any]) -> str:
        return str(
            item.get("name")
            or item.get("server_name")
            or item.get("title")
            or item.get("id")
            or ""
        )

    def _get_id(self, item: Dict[str, Any]) -> str:
        return str(item.get("id") or item.get("_id") or item.get("uuid") or "")

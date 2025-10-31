from typing import Any, Dict, List, Optional, Tuple
import os
import re
import requests
from urllib.parse import urljoin


class SimpleRegistryClient:
    """Simple client for querying MCP registries for server discovery."""

    DEFAULT_DEMO_REGISTRY = "https://registry.mcp.run/"

    def __init__(self, registry_url: Optional[str] = None):
        """Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        """
        base = registry_url or os.environ.get(
            "MCP_REGISTRY_URL") or self.DEFAULT_DEMO_REGISTRY
        if not base.endswith("/"):
            base = base + "/"
        self.base_url = base
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "SimpleRegistryClient/1.0"
        })
        self.timeout = 20

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """List all available servers in the registry.
        Args:
            limit (int, optional): Maximum number of entries to return. Defaults to 100.
            cursor (str, optional): Pagination cursor for retrieving next set of results.
        Returns:
            Tuple[List[Dict[str, Any]], Optional[str]]: List of server metadata dictionaries and the next cursor if available.
        Raises:
            requests.RequestException: If the request fails.
        """
        params: Dict[str, Any] = {"limit": limit}
        if cursor is not None:
            params["cursor"] = cursor

        payload = self._get_json_with_fallback(
            paths=["servers", "api/servers"],
            params=params
        )
        servers, next_cursor = self._extract_list_and_cursor(payload)
        return servers, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        """Search for servers in the registry.
        Args:
            query (str): Search query string.
        Returns:
            List[Dict[str, Any]]: List of matching server metadata dictionaries.
        Raises:
            requests.RequestException: If the request fails.
        """
        # Try common search endpoints, then fall back to filtered list endpoint variants.
        candidates = [
            ("servers/search", {"q": query}),
            ("api/servers/search", {"q": query}),
            ("servers", {"search": query}),
            ("api/servers", {"search": query}),
            ("servers", {"q": query}),
            ("api/servers", {"q": query}),
        ]

        last_error: Optional[Exception] = None
        for path, params in candidates:
            try:
                payload = self._get_json(path, params=params)
                items, _ = self._extract_list_and_cursor(payload)
                if items:
                    return items
                # If endpoint returns no items but is valid, still return empty.
                if isinstance(payload, (dict, list)):
                    return items
            except requests.RequestException as e:
                last_error = e
                continue

        if last_error:
            raise last_error
        return []

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific server.
        Args:
            server_id (str): ID of the server.
        Returns:
            Dict[str, Any]: Server metadata dictionary.
        Raises:
            requests.RequestException: If the request fails.
            ValueError: If the server is not found.
        """
        candidates = [f"servers/{server_id}", f"api/servers/{server_id}"]
        last_status = None
        last_exc: Optional[Exception] = None
        for path in candidates:
            try:
                payload = self._get_json(path)
                if isinstance(payload, dict):
                    if "server" in payload and isinstance(payload["server"], dict):
                        return payload["server"]
                    return payload
                if isinstance(payload, list) and payload:
                    first = payload[0]
                    return first if isinstance(first, dict) else {"data": payload}
                return {}
            except requests.HTTPError as e:
                last_exc = e
                if e.response is not None:
                    last_status = e.response.status_code
                    if e.response.status_code == 404:
                        raise ValueError(f"Server '{server_id}' not found")
                continue
            except requests.RequestException as e:
                last_exc = e
                continue

        if last_status == 404:
            raise ValueError(f"Server '{server_id}' not found")
        if last_exc:
            raise last_exc
        raise ValueError(f"Server '{server_id}' not found")

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a server by its name.
        Args:
            name (str): Name of the server to find.
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        """
        results = self.search_servers(name)
        exact_matches: List[Dict[str, Any]] = []
        name_lower = name.lower()

        for item in results:
            item_name = self._extract_name(item)
            if item_name == name:
                exact_matches.append(item)

        if not exact_matches:
            for item in results:
                item_name = self._extract_name(item)
                if item_name.lower() == name_lower:
                    exact_matches.append(item)

        return exact_matches[0] if exact_matches else None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        """Find a server by exact name match or server ID.
        This is a simple, efficient lookup that only makes network requests when necessary:
        1. Server ID (UUID format) - direct API call
        2. Exact name match from server list - single additional API call
        Args:
            reference (str): Server reference (ID or exact name).
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        """
        if self._looks_like_uuid(reference):
            try:
                return self.get_server_info(reference)
            except ValueError:
                return None

        return self.get_server_by_name(reference)

    def _get_json_with_fallback(self, paths: List[str], params: Optional[Dict[str, Any]] = None) -> Any:
        last_error: Optional[Exception] = None
        for path in paths:
            try:
                return self._get_json(path, params=params)
            except requests.RequestException as e:
                last_error = e
                continue
        if last_error:
            raise last_error
        raise requests.RequestException("No valid endpoint available")

    def _get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = urljoin(self.base_url, path)
        resp = self.session.get(url, params=params or {}, timeout=self.timeout)
        resp.raise_for_status()
        if not resp.content:
            return {}
        return resp.json()

    @staticmethod
    def _extract_list_and_cursor(payload: Any) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        items: List[Dict[str, Any]] = []
        next_cursor: Optional[str] = None

        if isinstance(payload, list):
            items = [x for x in payload if isinstance(x, dict)]
            return items, None

        if isinstance(payload, dict):
            candidates = [
                "servers", "items", "results", "data", "entries", "list"
            ]
            for key in candidates:
                val = payload.get(key)
                if isinstance(val, list):
                    items = [x for x in val if isinstance(x, dict)]
                    break
                if isinstance(val, dict) and "items" in val and isinstance(val["items"], list):
                    items = [x for x in val["items"] if isinstance(x, dict)]
                    break

            cursor_keys = ["next", "next_cursor", "cursor",
                           "nextCursor", "nextPageCursor", "page.next"]
            for ck in cursor_keys:
                if ck in payload and isinstance(payload[ck], str):
                    next_cursor = payload[ck]
                    break
            if next_cursor is None and "page" in payload and isinstance(payload["page"], dict):
                page = payload["page"]
                for ck in ["next", "cursor", "next_cursor", "nextCursor"]:
                    if ck in page and isinstance(page[ck], str):
                        next_cursor = page[ck]
                        break

        return items, next_cursor

    @staticmethod
    def _extract_name(item: Dict[str, Any]) -> str:
        for key in ("name", "display_name", "displayName", "title"):
            if key in item and isinstance(item[key], str):
                return item[key]
        return item.get("id", "")

    @staticmethod
    def _looks_like_uuid(value: str) -> bool:
        uuid_regex = re.compile(
            r"^[0-9a-fA-F]{8}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{12}$"
        )
        return bool(uuid_regex.match(value))

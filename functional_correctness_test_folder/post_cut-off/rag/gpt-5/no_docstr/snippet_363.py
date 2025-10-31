import os
import re
import requests
from typing import Any, Dict, List, Optional, Tuple


class SimpleRegistryClient:
    """Simple client for querying MCP registries for server discovery."""

    def __init__(self, registry_url: Optional[str] = None):
        """Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        """
        env_url = os.environ.get("MCP_REGISTRY_URL")
        default_url = "https://registry.modelcontextprotocol.io"
        base_url = registry_url or env_url or default_url
        self.registry_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "SimpleRegistryClient/1.0"})
        self.timeout = float(os.environ.get("MCP_REGISTRY_TIMEOUT", "10"))

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.registry_url}{path}"
        resp = self.session.get(url, params=params or {}, timeout=self.timeout)
        return resp

    @staticmethod
    def _extract_list_and_cursor(data: Any) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        items: List[Dict[str, Any]] = []
        next_cursor: Optional[str] = None

        # Direct list response
        if isinstance(data, list):
            items = data
            return items, None

        if not isinstance(data, dict):
            return items, None

        # Common list containers
        if "servers" in data and isinstance(data["servers"], list):
            items = data["servers"]
        elif "items" in data and isinstance(data["items"], list):
            items = data["items"]
        elif "results" in data and isinstance(data["results"], dict):
            res = data["results"]
            if "servers" in res and isinstance(res["servers"], list):
                items = res["servers"]
            elif "items" in res and isinstance(res["items"], list):
                items = res["items"]

            # Cursor inside results
            next_cursor = (
                res.get("nextCursor")
                or res.get("cursor")
                or res.get("next")
                or res.get("next_page_cursor")
            )

        else:
            # Fallback: single object may be wrapped
            if "server" in data and isinstance(data["server"], dict):
                items = [data["server"]]

        # Top-level cursor keys
        if next_cursor is None and isinstance(data, dict):
            next_cursor = (
                data.get("nextCursor")
                or data.get("cursor")
                or data.get("next")
                or (data.get("pageInfo", {}) or {}).get("nextCursor")
                or (data.get("pagination", {}) or {}).get("next_cursor")
                or data.get("next_page_cursor")
            )

        return items, next_cursor

    @staticmethod
    def _unwrap_server(data: Any) -> Dict[str, Any]:
        if isinstance(data, dict):
            if "server" in data and isinstance(data["server"], dict):
                return data["server"]
            return data
        return {}

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
        if cursor:
            params["cursor"] = cursor

        resp = self._get("/servers", params=params)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            # Some registries may not support /servers; try root index as fallback
            if resp.status_code == 404:
                alt = self._get("/", params=params)
                alt.raise_for_status()
                data = alt.json()
                items, next_cursor = self._extract_list_and_cursor(data)
                return items, next_cursor
            raise e

        data = resp.json()
        items, next_cursor = self._extract_list_and_cursor(data)
        return items, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        """Search for servers in the registry.
        Args:
            query (str): Search query string.
        Returns:
            List[Dict[str, Any]]: List of matching server metadata dictionaries.
        Raises:
            requests.RequestException: If the request fails.
        """
        # Try explicit search endpoint
        try:
            resp = self._get("/servers/search", params={"q": query})
            if resp.status_code == 404:
                raise requests.HTTPError(response=resp)
            resp.raise_for_status()
            data = resp.json()
            items, _ = self._extract_list_and_cursor(data)
            if items:
                return items
        except requests.RequestException:
            pass

        # Fallback: servers endpoint with query param (if supported)
        try:
            resp = self._get("/servers", params={"q": query, "limit": 100})
            # If servers supports q, use that, else we'll filter client-side below
            if resp.ok:
                data = resp.json()
                items, _ = self._extract_list_and_cursor(data)
                # If registry returned items, prefer them
                if items:
                    return items
        except requests.RequestException:
            pass

        # Final fallback: list and client-side filter
        # Fetch up to a reasonable number of pages
        results: List[Dict[str, Any]] = []
        cursor: Optional[str] = None
        visited_pages = 0
        max_pages = 5
        q = query.lower()
        while visited_pages < max_pages:
            items, cursor = self.list_servers(limit=200, cursor=cursor)
            for it in items:
                name = str(it.get("name", "")).lower()
                title = str(it.get("title", "")).lower()
                desc = str(it.get("description", "")).lower()
                tags = it.get("tags", [])
                tags_text = " ".join([str(t) for t in tags]).lower(
                ) if isinstance(tags, list) else str(tags).lower()
                if q in name or q in title or q in desc or q in tags_text:
                    results.append(it)
            visited_pages += 1
            if not cursor:
                break

        return results

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
        resp = self._get(f"/servers/{server_id}")
        if resp.status_code == 404:
            raise ValueError(f"Server not found: {server_id}")
        resp.raise_for_status()
        data = resp.json()
        server = self._unwrap_server(data)
        if not server:
            raise ValueError(
                f"Server not found or invalid response for: {server_id}")
        return server

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a server by its name.
        Args:
            name (str): Name of the server to find.
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        """
        # Prefer search API for efficiency
        try:
            candidates = self.search_servers(name)
            for s in candidates:
                s_name = str(s.get("name") or s.get("title") or "").strip()
                if s_name.lower() == name.lower():
                    return s
        except requests.RequestException:
            pass

        # Fallback: list and exact match
        cursor: Optional[str] = None
        while True:
            items, cursor = self.list_servers(limit=200, cursor=cursor)
            for it in items:
                it_name = str(it.get("name") or it.get("title") or "").strip()
                if it_name.lower() == name.lower():
                    return it
            if not cursor:
                break
        return None

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
        # Check UUID-like pattern
        uuid_like = bool(re.fullmatch(
            r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}", reference))
        if uuid_like:
            try:
                return self.get_server_info(reference)
            except ValueError:
                return None

        # Single call: list many and exact-match by name
        items, _ = self.list_servers(limit=1000, cursor=None)
        for it in items:
            it_name = str(it.get("name") or it.get("title") or "").strip()
            if it_name.lower() == reference.lower():
                return it
        return None

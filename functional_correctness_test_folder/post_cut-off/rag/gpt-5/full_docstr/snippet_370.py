from typing import Any, Dict, List, Optional, Tuple
import os
import uuid
import requests


class SimpleRegistryClient:
    """Simple client for querying MCP registries for server discovery."""

    DEFAULT_REGISTRY_URL = "https://registry.modelcontextprotocol.io"

    def __init__(self, registry_url: Optional[str] = None):
        """Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        """
        base = registry_url or os.environ.get(
            "MCP_REGISTRY_URL") or self.DEFAULT_REGISTRY_URL
        # Normalize URL by stripping redundant trailing slash
        self.base_url = base.rstrip("/")
        self.session = requests.Session()
        self.timeout = 10

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
        # Primary endpoint
        url = f"{self.base_url}/servers"
        params: Dict[str, Any] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        resp = self.session.get(url, params=params, timeout=self.timeout)
        # Allow 404 to bubble as HTTPError; caller expects RequestException on request failure
        resp.raise_for_status()

        data = resp.json()
        items = self._extract_items(data)
        next_cursor = self._extract_next_cursor(data)
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
        # Try a dedicated search endpoint first
        endpoints = [
            (f"{self.base_url}/servers/search", {"q": query}),
            (f"{self.base_url}/servers/search", {"query": query}),
            (f"{self.base_url}/servers", {"q": query}),
            (f"{self.base_url}/search", {"q": query}),
            (f"{self.base_url}/search", {"query": query}),
        ]

        for url, params in endpoints:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            if resp.status_code == 404:
                continue
            resp.raise_for_status()
            data = resp.json()
            items = self._extract_items(data)
            if items:
                return items

        # Fallback: client-side filter over paginated listing
        results: List[Dict[str, Any]] = []
        cursor: Optional[str] = None
        q = query.lower()
        for _ in range(20):  # safety cap on number of pages
            page, cursor = self.list_servers(limit=200, cursor=cursor)
            for item in page:
                if self._matches_query(item, q):
                    results.append(item)
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
        url = f"{self.base_url}/servers/{server_id}"
        resp = self.session.get(url, timeout=self.timeout)
        if resp.status_code == 404:
            raise ValueError(f"Server not found: {server_id}")
        resp.raise_for_status()
        return resp.json()

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a server by its name.
        Args:
            name (str): Name of the server to find.
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        """
        target = name.strip().lower()
        cursor: Optional[str] = None
        for _ in range(50):  # safety cap
            page, cursor = self.list_servers(limit=200, cursor=cursor)
            for item in page:
                if self._extract_name(item).lower() == target:
                    return item
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
        ref = reference.strip()
        if self._is_uuid(ref):
            try:
                return self.get_server_info(ref)
            except ValueError:
                return None

        # Single list call for exact name match
        page, _ = self.list_servers(limit=1000, cursor=None)
        target = ref.lower()
        for item in page:
            if self._extract_name(item).lower() == target:
                return item
        return None

    @staticmethod
    def _is_uuid(value: str) -> bool:
        try:
            uuid.UUID(value)
            return True
        except (ValueError, AttributeError, TypeError):
            return False

    @staticmethod
    def _extract_items(data: Any) -> List[Dict[str, Any]]:
        if isinstance(data, list):
            return data  # already a list of items
        if not isinstance(data, dict):
            return []
        for key in ("items", "servers", "results", "data"):
            v = data.get(key)
            if isinstance(v, list):
                return v
        # Some APIs wrap under {"data": {"items": [...]}}
        nested = data.get("data")
        if isinstance(nested, dict):
            for key in ("items", "servers", "results"):
                v = nested.get(key)
                if isinstance(v, list):
                    return v
        return []

    @staticmethod
    def _extract_next_cursor(data: Any) -> Optional[str]:
        if not isinstance(data, dict):
            return None
        for key in ("next_cursor", "nextCursor", "cursor", "next"):
            v = data.get(key)
            if isinstance(v, str) and v:
                return v
        nested = data.get("page") or data.get("pagination")
        if isinstance(nested, dict):
            for key in ("next_cursor", "nextCursor", "cursor", "next"):
                v = nested.get(key)
                if isinstance(v, str) and v:
                    return v
        return None

    @staticmethod
    def _extract_name(item: Dict[str, Any]) -> str:
        return str(item.get("name") or item.get("title") or item.get("display_name") or item.get("id") or "")

    @staticmethod
    def _matches_query(item: Dict[str, Any], q: str) -> bool:
        fields = [
            str(item.get("name") or ""),
            str(item.get("title") or ""),
            str(item.get("display_name") or ""),
            str(item.get("description") or ""),
            str(item.get("summary") or ""),
        ]
        # tags may be list or string
        tags = item.get("tags")
        if isinstance(tags, list):
            fields.extend([str(t) for t in tags])
        elif isinstance(tags, str):
            fields.append(tags)
        content = " ".join(fields).lower()
        return q in content

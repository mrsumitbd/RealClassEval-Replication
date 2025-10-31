from typing import Optional, Tuple, List, Dict, Any
import os
import re
import uuid
import requests


class SimpleRegistryClient:
    """Simple client for querying MCP registries for server discovery."""

    DEFAULT_REGISTRY_URL = "https://registry.modelcontextprotocol.dev"

    def __init__(self, registry_url: Optional[str] = None):
        """Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        """
        base_url = registry_url or os.environ.get(
            "MCP_REGISTRY_URL") or self.DEFAULT_REGISTRY_URL
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.timeout = 15

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

        url = f"{self.base_url}/servers"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        items, next_cursor = self._extract_items_and_cursor(data)
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
        # Try common search endpoints in order.
        endpoints = [
            ("/servers/search", {"q": query}),
            ("/servers/search", {"query": query}),
            ("/search", {"q": query}),
            ("/search", {"query": query}),
        ]

        last_exc: Optional[requests.RequestException] = None
        for path, params in endpoints:
            url = f"{self.base_url}{path}"
            try:
                resp = self.session.get(
                    url, params=params, timeout=self.timeout)
                if resp.status_code == 404:
                    continue
                resp.raise_for_status()
                data = resp.json()
                items, _ = self._extract_items_and_cursor(data)
                if items:
                    return items
                # If endpoint returns no items but not an error, continue trying others.
            except requests.RequestException as exc:
                last_exc = exc
                continue

        # Fallback: single page list + simple filter
        try:
            items, _ = self.list_servers(limit=1000)
            q = query.lower()
            results: List[Dict[str, Any]] = []
            for it in items:
                name = str(it.get("name", "")).lower()
                desc = str(it.get("description", "")).lower()
                if q in name or q in desc:
                    results.append(it)
            return results
        except requests.RequestException as exc:
            # If we had a previous exception, raise that, else raise this one.
            raise (last_exc or exc)

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
        data = resp.json()
        if isinstance(data, dict) and "server" in data:
            return data["server"]
        return data

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a server by its name.
        Args:
            name (str): Name of the server to find.
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        """
        # Prefer search endpoint for efficiency and accuracy.
        results = self.search_servers(name)
        name_lower = name.lower()
        for it in results:
            if str(it.get("name", "")).lower() == name_lower:
                return it
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
        if self._looks_like_uuid(reference):
            try:
                return self.get_server_info(reference)
            except ValueError:
                return None

        items, _ = self.list_servers(limit=1000)
        ref_lower = reference.lower()
        for it in items:
            if str(it.get("name", "")).lower() == ref_lower:
                return it
        return None

    def _extract_items_and_cursor(self, data: Any) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        if isinstance(data, list):
            return data, None
        if not isinstance(data, dict):
            return [], None

        items = (
            data.get("servers")
            or data.get("items")
            or data.get("results")
            or data.get("data")
            or []
        )
        if not isinstance(items, list):
            items = []

        # Try various locations for next cursor
        next_cursor = (
            data.get("next_cursor")
            or data.get("cursor")
            or (data.get("pagination") or {}).get("next_cursor")
            or (data.get("meta") or {}).get("next_cursor")
            or (data.get("next") or {}).get("cursor")
        )
        return items, next_cursor

    def _looks_like_uuid(self, s: str) -> bool:
        if not isinstance(s, str):
            return False
        if not re.fullmatch(r"[0-9a-fA-F-]{36}", s):
            return False
        try:
            uuid.UUID(s)
            return True
        except ValueError:
            return False

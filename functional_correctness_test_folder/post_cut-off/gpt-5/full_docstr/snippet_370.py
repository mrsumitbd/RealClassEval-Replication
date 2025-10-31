from typing import Optional, Tuple, List, Dict, Any
import os
import uuid
from urllib.parse import urljoin
import requests


class SimpleRegistryClient:
    '''Simple client for querying MCP registries for server discovery.'''

    DEFAULT_REGISTRY_URL = "https://registry.mcp.dev/"

    def __init__(self, registry_url: Optional[str] = None):
        '''Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        '''
        base = registry_url or os.environ.get(
            "MCP_REGISTRY_URL") or self.DEFAULT_REGISTRY_URL
        if not base.endswith("/"):
            base = base + "/"
        self.base_url = base
        self.session = requests.Session()
        self.timeout = (10, 30)

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        '''List all available servers in the registry.
        Args:
            limit (int, optional): Maximum number of entries to return. Defaults to 100.
            cursor (str, optional): Pagination cursor for retrieving next set of results.
        Returns:
            Tuple[List[Dict[str, Any]], Optional[str]]: List of server metadata dictionaries and the next cursor if available.
        Raises:
            requests.RequestException: If the request fails.
        '''
        params: Dict[str, Any] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        url = urljoin(self.base_url, "servers")
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json() if resp.content else {}
        items = (
            data.get("items")
            or data.get("servers")
            or data.get("results")
            or []
        )
        next_cursor = (
            data.get("nextCursor")
            or data.get("next_cursor")
            or data.get("cursor")
            or None
        )
        return items, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        '''Search for servers in the registry.
        Args:
            query (str): Search query string.
        Returns:
            List[Dict[str, Any]]: List of matching server metadata dictionaries.
        Raises:
            requests.RequestException: If the request fails.
        '''
        # Prefer /servers/search?q=..., fallback to /servers?query=...
        url_search = urljoin(self.base_url, "servers/search")
        params = {"q": query}
        resp = self.session.get(
            url_search, params=params, timeout=self.timeout)
        if resp.status_code == 404:
            url_alt = urljoin(self.base_url, "servers")
            params = {"query": query}
            resp = self.session.get(
                url_alt, params=params, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json() if resp.content else {}
        return data.get("items") or data.get("servers") or data.get("results") or []

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        '''Get detailed information about a specific server.
        Args:
            server_id (str): ID of the server.
        Returns:
            Dict[str, Any]: Server metadata dictionary.
        Raises:
            requests.RequestException: If the request fails.
            ValueError: If the server is not found.
        '''
        url = urljoin(self.base_url, f"servers/{server_id}")
        resp = self.session.get(url, timeout=self.timeout)
        if resp.status_code == 404:
            raise ValueError(f"Server not found: {server_id}")
        resp.raise_for_status()
        data = resp.json() if resp.content else {}
        return data

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        '''Find a server by its name.
        Args:
            name (str): Name of the server to find.
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        '''
        cursor: Optional[str] = None
        while True:
            items, cursor = self.list_servers(limit=200, cursor=cursor)
            for item in items:
                item_name = item.get("name") or item.get(
                    "title") or item.get("display_name")
                if item_name == name or (isinstance(item_name, str) and item_name.lower() == name.lower()):
                    server_id = item.get("id") or item.get(
                        "server_id") or item.get("uuid")
                    if server_id:
                        try:
                            return self.get_server_info(server_id)
                        except ValueError:
                            return None
                    return item
            if not cursor:
                break
        return None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        '''Find a server by exact name match or server ID.
        This is a simple, efficient lookup that only makes network requests when necessary:
        1. Server ID (UUID format) - direct API call
        2. Exact name match from server list - single additional API call
        Args:
            reference (str): Server reference (ID or exact name).
        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.
        Raises:
            requests.RequestException: If the request fails.
        '''
        def is_uuid(s: str) -> bool:
            try:
                u = uuid.UUID(s)
                return str(u) == s.lower()
            except Exception:
                return False

        if is_uuid(reference):
            try:
                return self.get_server_info(reference)
            except ValueError:
                return None

        items, _ = self.list_servers(limit=1000)
        for item in items:
            item_name = item.get("name") or item.get(
                "title") or item.get("display_name")
            if item_name == reference:
                server_id = item.get("id") or item.get(
                    "server_id") or item.get("uuid")
                if server_id:
                    try:
                        return self.get_server_info(server_id)
                    except ValueError:
                        return None
                return item
        return None

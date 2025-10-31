from typing import Optional, List, Dict, Any, Tuple
import os
import requests
from urllib.parse import urljoin
import re


class SimpleRegistryClient:
    def __init__(self, registry_url: Optional[str] = None):
        '''Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        '''
        self.registry_url = (
            registry_url
            or os.getenv("MCP_REGISTRY_URL")
            or "https://registry.modelcontextprotocol.io"
        ).rstrip("/")
        self.session = requests.Session()
        self.timeout = 15

    def _build_url(self, path: str) -> str:
        return urljoin(self.registry_url + "/", path.lstrip("/"))

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        params: Dict[str, Any] = {"limit": max(1, int(limit))}
        if cursor:
            params["cursor"] = cursor

        url = self._build_url("/servers")
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json() or {}

        items = data.get("items")
        if items is None and isinstance(data, list):
            items = data
        if items is None:
            items = []

        next_cursor = data.get("nextCursor", data.get("next_cursor"))
        if next_cursor == "":
            next_cursor = None

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
        url = self._build_url("/servers/search")
        resp = self.session.get(url, params={"q": query}, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json() or {}
        if isinstance(data, list):
            return data
        return data.get("items", [])

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        url = self._build_url(f"/servers/{server_id}")
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json() or {}

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        results = self.search_servers(name)
        for item in results:
            if isinstance(item, dict) and item.get("name") == name:
                return item
        # Fallback to exact match from first page of list
        items, _ = self.list_servers(limit=200)
        for item in items:
            if isinstance(item, dict) and item.get("name") == name:
                return item
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
        uuid_regex = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )

        if uuid_regex.match(reference):
            try:
                return self.get_server_info(reference)
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 404:
                    return None
                raise

        items, _ = self.list_servers(limit=200)
        for item in items:
            if isinstance(item, dict) and item.get("name") == reference:
                return item
        return None

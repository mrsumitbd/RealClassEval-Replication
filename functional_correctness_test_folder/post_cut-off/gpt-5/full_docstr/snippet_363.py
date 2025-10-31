import os
import re
from typing import Any, Dict, List, Optional, Tuple

import requests


class SimpleRegistryClient:
    '''Simple client for querying MCP registries for server discovery.'''

    DEFAULT_REGISTRY_URL = "https://registry.modelcontextprotocol.io"
    ENV_VAR = "MCP_REGISTRY_URL"

    def __init__(self, registry_url: Optional[str] = None):
        '''Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        '''
        base = registry_url or os.environ.get(
            self.ENV_VAR) or self.DEFAULT_REGISTRY_URL
        self.base_url = base.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.timeout = 15

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
        url = f"{self.base_url}/servers"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        try:
            resp.raise_for_status()
        except requests.RequestException:
            raise
        data = resp.json()
        items = data.get("items") or data.get(
            "servers") or data.get("data") or []
        next_cursor = data.get("next_cursor") or data.get(
            "nextCursor") or data.get("cursor") or None
        if not isinstance(items, list):
            items = []
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
        # Prefer a conventional search endpoint under /servers
        url_candidates = [
            f"{self.base_url}/servers/search",
            f"{self.base_url}/search",
        ]
        last_exc: Optional[requests.RequestException] = None
        for url in url_candidates:
            try:
                resp = self.session.get(
                    url, params={"q": query, "query": query}, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                items = data.get("items") or data.get(
                    "servers") or data.get("results") or []
                return items if isinstance(items, list) else []
            except requests.RequestException as e:
                last_exc = e
                continue
        if last_exc:
            raise last_exc
        return []

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
        url = f"{self.base_url}/servers/{server_id}"
        resp = self.session.get(url, timeout=self.timeout)
        if resp.status_code == 404:
            raise ValueError(f"Server not found: {server_id}")
        try:
            resp.raise_for_status()
        except requests.RequestException:
            raise
        data = resp.json()
        if isinstance(data, dict) and ("id" in data or "name" in data):
            return data
        if isinstance(data, dict) and "server" in data and isinstance(data["server"], dict):
            return data["server"]
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
                if not isinstance(item, dict):
                    continue
                n = item.get("name") or item.get(
                    "title") or item.get("displayName")
                if n == name:
                    # If an ID is present, fetch full details for consistency
                    server_id = item.get("id") or item.get(
                        "server_id") or item.get("uuid")
                    if server_id:
                        try:
                            return self.get_server_info(str(server_id))
                        except (requests.RequestException, ValueError):
                            return item
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
        uuid_regex = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        if uuid_regex.match(reference):
            try:
                return self.get_server_info(reference)
            except (requests.RequestException, ValueError):
                pass
        return self.get_server_by_name(reference)

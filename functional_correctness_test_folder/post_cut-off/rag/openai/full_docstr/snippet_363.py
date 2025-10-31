
import os
import re
from typing import Any, Dict, List, Optional, Tuple

import requests


class SimpleRegistryClient:
    """Simple client for querying MCP registries for server discovery."""

    _DEFAULT_REGISTRY_URL = "https://demo.mcp.registry.com"

    def __init__(self, registry_url: Optional[str] = None):
        """
        Initialize the registry client.

        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        """
        self.registry_url = (
            registry_url
            or os.getenv("MCP_REGISTRY_URL")
            or self._DEFAULT_REGISTRY_URL
        )
        # Ensure no trailing slash
        self.registry_url = self.registry_url.rstrip("/")

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.registry_url}{path}"
        resp = requests.request(method, url, params=params, timeout=10)
        resp.raise_for_status()
        return resp

    def list_servers(
        self, limit: int = 100, cursor: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        List all available servers in the registry.

        Args:
            limit (int, optional): Maximum number of entries to return. Defaults to 100.
            cursor (str, optional): Pagination cursor for retrieving next set of results.

        Returns:
            Tuple[List[Dict[str, Any]], Optional[str]]: List of server metadata dictionaries and the next cursor if available.

        Raises:
            requests.RequestException: If the request fails.
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        resp = self._request("GET", "/servers", params=params)
        data = resp.json()
        servers = data.get("servers", [])
        next_cursor = data.get("next_cursor")
        return servers, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for servers in the registry.

        Args:
            query (str): Search query string.

        Returns:
            List[Dict[str, Any]]: List of matching server metadata dictionaries.

        Raises:
            requests.RequestException: If the request fails.
        """
        params = {"q": query}
        resp = self._request("GET", "/servers/search", params=params)
        data = resp.json()
        return data.get("servers", [])

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific server.

        Args:
            server_id (str): ID of the server.

        Returns:
            Dict[str, Any]: Server metadata dictionary.

        Raises:
            requests.RequestException: If the request fails.
            ValueError: If the server is not found.
        """
        try:
            resp = self._request("GET", f"/servers/{server_id}")
            return resp.json()
        except requests.HTTPError as exc:
            if exc.response.status_code == 404:
                raise ValueError(f"Server {server_id} not found") from exc
            raise

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Find a server by its name.

        Args:
            name (str): Name of the server to find.

        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.

        Raises:
            requests.RequestException: If the request fails.
        """
        cursor = None
        while True:
            servers, cursor = self.list_servers(limit=100, cursor=cursor)
            for srv in servers:
                if srv.get("name") == name:
                    return srv
            if not cursor:
                break
        return None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        """
        Find a server by exact name match or server ID.

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
        # Simple UUID regex
        uuid_regex = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        if uuid_regex.match(reference):
            try:
                return self.get_server_info(reference)
            except ValueError:
                return None

        # Treat as name
        return self.get_server_by_name(reference)

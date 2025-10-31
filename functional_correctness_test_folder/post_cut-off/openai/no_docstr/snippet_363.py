
from typing import Any, Dict, List, Optional, Tuple
import requests


class SimpleRegistryClient:
    """
    A minimal client for interacting with a registry service.
    """

    def __init__(self, registry_url: Optional[str] = None):
        """
        Initialize the client with an optional registry base URL.
        If no URL is provided, a default is used.
        """
        self.registry_url = registry_url or "https://registry.example.com"
        self.session = requests.Session()

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Internal helper to perform a GET request and return JSON.
        Raises an exception if the request fails or the response is not JSON.
        """
        url = f"{self.registry_url.rstrip('/')}/{path.lstrip('/')}"
        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def list_servers(
        self, limit: int = 100, cursor: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Retrieve a paginated list of servers.

        Returns a tuple of (list_of_servers, next_cursor).
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        data = self._get("/servers", params=params)
        servers = data.get("servers", [])
        next_cursor = data.get("cursor")
        return servers, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for servers matching the given query string.
        """
        params = {"q": query}
        data = self._get("/servers/search", params=params)
        return data.get("servers", [])

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        """
        Retrieve detailed information for a specific server by its ID.
        """
        return self._get(f"/servers/{server_id}")

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Find a server by its name. Returns the first match or None.
        """
        # Attempt to search by name first
        results = self.search_servers(name)
        for server in results:
            if server.get("name") == name:
                return server

        # Fallback: iterate through all servers
        cursor = None
        while True:
            servers, cursor = self.list_servers(cursor=cursor)
            for server in servers:
                if server.get("name") == name:
                    return server
            if not cursor:
                break
        return None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        """
        Find a server by a unique reference string.
        """
        # Assume the registry supports filtering by reference
        params = {"reference": reference}
        data = self._get("/servers", params=params)
        servers = data.get("servers", [])
        if servers:
            return servers[0]
        return None

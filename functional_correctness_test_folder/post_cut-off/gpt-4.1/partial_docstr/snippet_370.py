
import os
import requests
from typing import Optional, List, Dict, Any, Tuple
import uuid


class SimpleRegistryClient:

    DEFAULT_REGISTRY_URL = "https://demo.mcp.mls.srl/registry"

    def __init__(self, registry_url: Optional[str] = None):
        '''Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        '''
        if registry_url is not None:
            self.registry_url = registry_url.rstrip("/")
        else:
            self.registry_url = os.environ.get(
                "MCP_REGISTRY_URL", self.DEFAULT_REGISTRY_URL).rstrip("/")
        self.session = requests.Session()

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        url = f"{self.registry_url}/servers"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        servers = data.get("servers", [])
        next_cursor = data.get("next_cursor")
        return servers, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        '''Search for servers in the registry.
        Args:
            query (str): Search query string.
        Returns:
            List[Dict[str, Any]]: List of matching server metadata dictionaries.
        Raises:
            requests.RequestException: If the request fails.
        '''
        url = f"{self.registry_url}/servers/search"
        params = {"q": query}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("servers", [])

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        url = f"{self.registry_url}/servers/{server_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        # List all servers and find by exact name match
        cursor = None
        while True:
            servers, cursor = self.list_servers(limit=100, cursor=cursor)
            for server in servers:
                if server.get("name") == name:
                    return server
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
        # Check if reference is a valid UUID
        try:
            uuid_obj = uuid.UUID(reference)
            # If valid UUID, try to fetch by ID
            return self.get_server_info(reference)
        except (ValueError, requests.HTTPError):
            pass
        # Otherwise, try to find by name
        return self.get_server_by_name(reference)

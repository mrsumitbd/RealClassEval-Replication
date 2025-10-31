
import os
import requests
from typing import Optional, List, Dict, Any, Tuple
import uuid


class SimpleRegistryClient:
    '''Simple client for querying MCP registries for server discovery.'''

    DEFAULT_REGISTRY_URL = "https://registry.demo.mcp.example.com"

    def __init__(self, registry_url: Optional[str] = None):
        '''Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        '''
        self.registry_url = registry_url or os.getenv(
            'MCP_REGISTRY_URL', self.DEFAULT_REGISTRY_URL)

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
        params = {'limit': limit}
        if cursor:
            params['cursor'] = cursor

        response = requests.get(f"{self.registry_url}/servers", params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('servers', []), data.get('next_cursor')

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        '''Search for servers in the registry.
        Args:
            query (str): Search query string.
        Returns:
            List[Dict[str, Any]]: List of matching server metadata dictionaries.
        Raises:
            requests.RequestException: If the request fails.
        '''
        response = requests.get(
            f"{self.registry_url}/servers/search", params={'q': query})
        response.raise_for_status()
        return response.json().get('servers', [])

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
        response = requests.get(f"{self.registry_url}/servers/{server_id}")
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError(f"Server {server_id} not found")
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
        servers, _ = self.list_servers(
            limit=1000)  # Large limit to avoid pagination
        for server in servers:
            if server.get('name') == name:
                return server
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
        try:
            # Check if reference is a valid UUID (server ID)
            uuid.UUID(reference)
            return self.get_server_info(reference)
        except ValueError:
            # Not a UUID, treat as name
            return self.get_server_by_name(reference)


import os
import requests
from typing import Optional, List, Dict, Any, Tuple
import re


class SimpleRegistryClient:
    '''Simple client for querying MCP registries for server discovery.'''
    DEFAULT_REGISTRY_URL = "https://demo.mcp-registry.com/api"

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
        params = {'query': query}
        response = requests.get(f"{self.registry_url}/search", params=params)
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
        if response.status_code == 404:
            raise ValueError("Server not found")
        response.raise_for_status()
        return response.json()

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        servers = self.list_servers()[0]
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
        # Check if reference is a UUID
        if re.match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$', reference):
            try:
                return self.get_server_info(reference)
            except ValueError:
                return None
        else:
            return self.get_server_by_name(reference)

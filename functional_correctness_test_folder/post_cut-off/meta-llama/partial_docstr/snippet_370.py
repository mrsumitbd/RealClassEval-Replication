
import os
import requests
from typing import Optional, List, Dict, Any, Tuple
import uuid


class SimpleRegistryClient:

    def __init__(self, registry_url: Optional[str] = None):
        '''Initialize the registry client.
        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        '''
        if registry_url is None:
            registry_url = os.environ.get(
                'MCP_REGISTRY_URL', 'https://demo-registry.mcp.com')
        self.registry_url = registry_url.strip('/')

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        params = {'limit': limit}
        if cursor:
            params['cursor'] = cursor
        response = requests.get(f'{self.registry_url}/servers', params=params)
        response.raise_for_status()
        data = response.json()
        return data['servers'], data.get('next_cursor')

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
            f'{self.registry_url}/servers/search', params={'query': query})
        response.raise_for_status()
        return response.json()['servers']

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        response = requests.get(f'{self.registry_url}/servers/{server_id}')
        response.raise_for_status()
        return response.json()

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        # Fetch a large number of servers
        servers, _ = self.list_servers(limit=1000)
        for server in servers:
            if server['name'] == name:
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
            uuid.UUID(reference)
            return self.get_server_info(reference)
        except ValueError:
            return self.get_server_by_name(reference)

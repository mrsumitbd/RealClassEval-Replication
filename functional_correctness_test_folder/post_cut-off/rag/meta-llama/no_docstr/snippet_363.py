
import os
import requests
from typing import Optional, List, Dict, Any, Tuple
import uuid
import logging


class SimpleRegistryClient:
    """Simple client for querying MCP registries for server discovery."""

    DEFAULT_REGISTRY_URL = 'https://demo-registry.example.com'
    REQUEST_TIMEOUT = 10  # seconds

    def __init__(self, registry_url: Optional[str] = None):
        """Initialize the registry client.

        Args:
            registry_url (str, optional): URL of the MCP registry.
                If not provided, uses the MCP_REGISTRY_URL environment variable
                or falls back to the default demo registry.
        """
        self.registry_url = registry_url or os.environ.get(
            'MCP_REGISTRY_URL', self.DEFAULT_REGISTRY_URL)
        self.logger = logging.getLogger(__name__)

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request to the registry API."""
        url = f'{self.registry_url}{endpoint}'
        try:
            response = requests.request(
                method, url, timeout=self.REQUEST_TIMEOUT, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f'Request to {url} failed: {e}')
            raise

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
        params = {'limit': limit}
        if cursor:
            params['cursor'] = cursor
        response = self._make_request('GET', '/servers', params=params)
        data = response.json()
        return data['servers'], data.get('next_cursor')

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        """Search for servers in the registry.

        Args:
            query (str): Search query string.

        Returns:
            List[Dict[str, Any]]: List of matching server metadata dictionaries.

        Raises:
            requests.RequestException: If the request fails.
        """
        response = self._make_request(
            'GET', '/servers/search', params={'query': query})
        return response.json()['servers']

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
        try:
            uuid.UUID(server_id)
        except ValueError:
            raise ValueError(f'Invalid server ID: {server_id}')
        response = self._make_request('GET', f'/servers/{server_id}')
        return response.json()

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a server by its name.

        Args:
            name (str): Name of the server to find.

        Returns:
            Optional[Dict[str, Any]]: Server metadata dictionary or None if not found.

        Raises:
            requests.RequestException: If the request fails.
        """
        servers, _ = self.list_servers(
            limit=1000)  # Fetch a large number of servers
        for server in servers:
            if server['name'] == name:
                return server
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
        try:
            # Check if reference is a valid UUID
            uuid.UUID(reference)
            return self.get_server_info(reference)
        except ValueError:
            # Not a UUID, try exact name match
            return self.get_server_by_name(reference)

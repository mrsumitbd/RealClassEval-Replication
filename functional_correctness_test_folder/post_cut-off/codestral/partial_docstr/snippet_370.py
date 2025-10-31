
import os
import requests
from typing import Optional, List, Dict, Any, Tuple
import uuid


class SimpleRegistryClient:

    DEFAULT_REGISTRY_URL = "https://demo.mcp-registry.org"

    def __init__(self, registry_url: Optional[str] = None):
        self.registry_url = registry_url or os.getenv(
            'MCP_REGISTRY_URL') or self.DEFAULT_REGISTRY_URL

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        params = {'limit': limit}
        if cursor:
            params['cursor'] = cursor
        response = requests.get(f"{self.registry_url}/servers", params=params)
        response.raise_for_status()
        data = response.json()
        return data['servers'], data.get('next_cursor')

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        response = requests.get(
            f"{self.registry_url}/servers/search", params={'q': query})
        response.raise_for_status()
        return response.json()['servers']

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        response = requests.get(f"{self.registry_url}/servers/{server_id}")
        response.raise_for_status()
        return response.json()

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        servers, _ = self.list_servers(limit=1000)
        for server in servers:
            if server['name'] == name:
                return server
        return None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        try:
            uuid.UUID(reference)
            return self.get_server_info(reference)
        except ValueError:
            return self.get_server_by_name(reference)


import os
import requests
from typing import Optional, List, Dict, Any, Tuple
import uuid


class SimpleRegistryClient:

    def __init__(self, registry_url: Optional[str] = None):
        self.registry_url = registry_url or os.getenv(
            'MCP_REGISTRY_URL', 'https://demo-registry.com/api')

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        params = {'limit': limit}
        if cursor:
            params['cursor'] = cursor
        response = requests.get(f"{self.registry_url}/servers", params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('servers', []), data.get('next_cursor')

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        params = {'query': query}
        response = requests.get(f"{self.registry_url}/search", params=params)
        response.raise_for_status()
        return response.json().get('results', [])

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        response = requests.get(f"{self.registry_url}/servers/{server_id}")
        response.raise_for_status()
        return response.json()

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        servers, _ = self.list_servers()
        for server in servers:
            if server.get('name') == name:
                return server
        return None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        if uuid.UUID(reference, version=4):
            try:
                return self.get_server_info(reference)
            except requests.RequestException:
                return None
        else:
            return self.get_server_by_name(reference)

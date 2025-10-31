
from typing import Optional, List, Dict, Any, Tuple
import requests


class SimpleRegistryClient:

    def __init__(self, registry_url: Optional[str] = None):
        self.registry_url = registry_url or 'https://registry.example.com/api'

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        params = {'limit': limit}
        if cursor:
            params['cursor'] = cursor
        response = requests.get(f'{self.registry_url}/servers', params=params)
        response.raise_for_status()
        data = response.json()
        return data['servers'], data.get('next_cursor')

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        response = requests.get(
            f'{self.registry_url}/servers/search', params={'query': query})
        response.raise_for_status()
        return response.json()['servers']

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        response = requests.get(f'{self.registry_url}/servers/{server_id}')
        response.raise_for_status()
        return response.json()

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        response = requests.get(
            f'{self.registry_url}/servers', params={'name': name})
        response.raise_for_status()
        data = response.json()
        servers = data['servers']
        return servers[0] if servers else None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        response = requests.get(
            f'{self.registry_url}/servers', params={'reference': reference})
        response.raise_for_status()
        data = response.json()
        servers = data['servers']
        return servers[0] if servers else None

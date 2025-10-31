
from typing import Optional, List, Dict, Any, Tuple
import requests


class SimpleRegistryClient:

    def __init__(self, registry_url: Optional[str] = None):
        self.registry_url = registry_url or "https://registry.example.com/api"
        if self.registry_url.endswith('/'):
            self.registry_url = self.registry_url[:-1]

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        params = {'limit': limit}
        if cursor:
            params['cursor'] = cursor
        url = f"{self.registry_url}/servers"
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        servers = data.get('servers', [])
        next_cursor = data.get('next_cursor')
        return servers, next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        params = {'q': query}
        url = f"{self.registry_url}/servers/search"
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get('servers', [])

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        url = f"{self.registry_url}/servers/{server_id}"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        params = {'name': name}
        url = f"{self.registry_url}/servers/by-name"
        resp = requests.get(url, params=params)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        params = {'reference': reference}
        url = f"{self.registry_url}/servers/by-reference"
        resp = requests.get(url, params=params)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()

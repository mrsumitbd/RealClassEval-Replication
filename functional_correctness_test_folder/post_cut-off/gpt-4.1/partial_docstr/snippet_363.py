
import os
import requests
from typing import Optional, List, Dict, Any, Tuple


class SimpleRegistryClient:
    '''Simple client for querying MCP registries for server discovery.'''

    DEFAULT_REGISTRY_URL = "https://demo.mcp.moe/registry"

    def __init__(self, registry_url: Optional[str] = None):
        '''Initialize the registry client.'''
        self.registry_url = (
            registry_url or
            os.environ.get("MCP_REGISTRY_URL") or
            self.DEFAULT_REGISTRY_URL
        )
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
        url = f"{self.registry_url}/servers/search"
        params = {"q": query}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("servers", [])

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        url = f"{self.registry_url}/servers/{server_id}"
        resp = self.session.get(url)
        if resp.status_code == 404:
            raise ValueError(f"Server with ID '{server_id}' not found.")
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
        import re
        uuid_re = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
        if uuid_re.match(reference):
            try:
                return self.get_server_info(reference)
            except ValueError:
                return None
        server = self.get_server_by_name(reference)
        return server

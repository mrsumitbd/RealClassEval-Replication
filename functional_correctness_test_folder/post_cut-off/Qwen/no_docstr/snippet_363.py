
from typing import Optional, List, Dict, Any, Tuple


class SimpleRegistryClient:

    def __init__(self, registry_url: Optional[str] = None):
        self.registry_url = registry_url
        self.servers = [
            {"id": "1", "name": "Server1", "reference": "ref1",
                "info": {"cpu": "4", "memory": "16GB"}},
            {"id": "2", "name": "Server2", "reference": "ref2",
                "info": {"cpu": "8", "memory": "32GB"}},
            {"id": "3", "name": "Server3", "reference": "ref3",
                "info": {"cpu": "2", "memory": "8GB"}},
        ]

    def list_servers(self, limit: int = 100, cursor: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        if cursor:
            start_index = int(cursor)
        else:
            start_index = 0
        end_index = start_index + limit
        next_cursor = str(end_index) if end_index < len(self.servers) else None
        return self.servers[start_index:end_index], next_cursor

    def search_servers(self, query: str) -> List[Dict[str, Any]]:
        return [server for server in self.servers if query.lower() in server['name'].lower()]

    def get_server_info(self, server_id: str) -> Dict[str, Any]:
        for server in self.servers:
            if server['id'] == server_id:
                return server['info']
        return {}

    def get_server_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        for server in self.servers:
            if server['name'] == name:
                return server
        return None

    def find_server_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        for server in self.servers:
            if server['reference'] == reference:
                return server
        return None

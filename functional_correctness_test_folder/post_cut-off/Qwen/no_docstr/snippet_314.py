
from typing import Optional, List, Dict, Any, Tuple


class DiscoveryMixin:

    def validate_server(self, server_name: str, app_context: Optional['AppContext'] = None) -> bool:
        if app_context is None:
            app_context = AppContext()
        servers_data, _ = self.get_servers_data(app_context)
        return any(server['name'] == server_name for server in servers_data)

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        if app_context is None:
            app_context = AppContext()
        # Simulated server data retrieval
        servers = [
            {'name': 'server1', 'status': 'active'},
            {'name': 'server2', 'status': 'inactive'},
            {'name': 'server3', 'status': 'active'}
        ]
        errors = []
        return servers, errors


class AppContext:
    def __init__(self):
        # Placeholder for any necessary context data
        pass

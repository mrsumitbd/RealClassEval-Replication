
from typing import Optional, List, Dict, Any, Tuple


class AppContext:
    def __init__(self, servers: Optional[List[Dict[str, Any]]] = None):
        self.servers = servers or []


class DiscoveryMixin:

    def validate_server(self, server_name: str, app_context: Optional[AppContext] = None) -> bool:
        servers = []
        if app_context and hasattr(app_context, 'servers'):
            servers = app_context.servers
        for server in servers:
            if server.get('name') == server_name:
                return True
        return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        servers = []
        if app_context and hasattr(app_context, 'servers'):
            servers = app_context.servers
        server_names = [server.get('name', '') for server in servers]
        return servers, server_names

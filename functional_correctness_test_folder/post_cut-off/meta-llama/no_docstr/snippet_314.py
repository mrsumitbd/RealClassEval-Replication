
from typing import Optional, List, Dict, Any, Tuple


class AppContext:
    # Assuming AppContext is defined elsewhere
    pass


class DiscoveryMixin:
    def validate_server(self, server_name: str, app_context: Optional[AppContext] = None) -> bool:
        servers_data, _ = self.get_servers_data(app_context)
        for server in servers_data:
            if server.get('name') == server_name:
                return True
        return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        # For demonstration purposes, assume we have some default data
        # In a real scenario, this data would likely come from a database or API call
        servers_data = [
            {'name': 'Server1', 'host': 'localhost', 'port': 8080},
            {'name': 'Server2', 'host': 'example.com', 'port': 80}
        ]
        errors = []
        if app_context is None:
            errors.append('App context is not provided')
        return servers_data, errors

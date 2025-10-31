
class DiscoveryMixin:

    def validate_server(self, server_name: str, app_context: Optional[AppContext] = None) -> bool:
        if app_context is None:
            app_context = AppContext()
        servers_data, _ = self.get_servers_data(app_context)
        for server in servers_data:
            if server.get('name') == server_name:
                return True
        return False

    def get_servers_data(self, app_context: Optional['AppContext'] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
        if app_context is None:
            app_context = AppContext()
        servers_data = []
        errors = []
        # Assuming there's a method to fetch server data from the app context
        try:
            servers_data = app_context.fetch_servers_data()
        except Exception as e:
            errors.append(str(e))
        return servers_data, errors

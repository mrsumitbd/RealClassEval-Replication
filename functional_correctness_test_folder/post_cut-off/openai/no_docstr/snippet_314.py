
from typing import Any, Dict, List, Optional, Tuple


class DiscoveryMixin:
    """
    Mixin providing discovery utilities for server validation and data retrieval.
    """

    def validate_server(self, server_name: str, app_context: Optional["AppContext"] = None) -> bool:
        """
        Validate that a server with the given name exists in the provided application context.

        Parameters
        ----------
        server_name : str
            The name of the server to validate.
        app_context : Optional[AppContext]
            The application context containing server information. If None, the method
            will attempt to use a global context if available.

        Returns
        -------
        bool
            True if the server exists, False otherwise.
        """
        if app_context is None:
            # Attempt to use a global context if one is defined
            try:
                from .app_context import global_app_context  # type: ignore
                app_context = global_app_context
            except Exception:
                return False

        # The context is expected to expose a `servers` mapping.
        servers = getattr(app_context, "servers", {})
        if not isinstance(servers, dict):
            return False

        return server_name in servers

    def get_servers_data(
        self, app_context: Optional["AppContext"] = None
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Retrieve server data and a list of server names from the application context.

        Parameters
        ----------
        app_context : Optional[AppContext]
            The application context containing server information. If None, the method
            will attempt to use a global context if available.

        Returns
        -------
        Tuple[List[Dict[str, Any]], List[str]]
            A tuple where the first element is a list of server data dictionaries
            and the second element is a list of server names.
        """
        if app_context is None:
            # Attempt to use a global context if one is defined
            try:
                from .app_context import global_app_context  # type: ignore
                app_context = global_app_context
            except Exception:
                return [], []

        servers = getattr(app_context, "servers", {})
        if not isinstance(servers, dict):
            return [], []

        server_names = list(servers.keys())
        server_data = [servers[name] for name in server_names]
        return server_data, server_names

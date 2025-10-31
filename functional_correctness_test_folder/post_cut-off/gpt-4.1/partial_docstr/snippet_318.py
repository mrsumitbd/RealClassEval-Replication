
from typing import Any, Callable, Dict, List, Optional


class PluginAPI:

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager', app_context: Optional['AppContext']):
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context

    @property
    def app_context(self) -> 'AppContext':
        if self._app_context is None:
            raise RuntimeError(
                "AppContext has not been set on this PluginAPI instance.")
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        # Delegate to plugin_manager's get_api_function if available
        if hasattr(self._plugin_manager, "get_api_function"):
            func = self._plugin_manager.get_api_function(name)
            if func is not None:
                return func
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def list_available_apis(self) -> List[Dict[str, Any]]:
        # Delegate to plugin_manager's list_available_apis if available
        if hasattr(self._plugin_manager, "list_available_apis"):
            return self._plugin_manager.list_available_apis()
        return []

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        if hasattr(self._plugin_manager, "register_event_listener"):
            self._plugin_manager.register_event_listener(
                event_name, callback, self._plugin_name)
        else:
            raise RuntimeError(
                "PluginManager does not support event listening.")

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        if hasattr(self._plugin_manager, "dispatch_event"):
            self._plugin_manager.dispatch_event(
                event_name, *args, _triggering_plugin=self._plugin_name, **kwargs)
        else:
            raise RuntimeError(
                "PluginManager does not support event dispatching.")

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        # Delegate to plugin_manager's get_plugin_html_pages if available
        if hasattr(self._plugin_manager, "get_plugin_html_pages"):
            return self._plugin_manager.get_plugin_html_pages(self._plugin_name)
        return []

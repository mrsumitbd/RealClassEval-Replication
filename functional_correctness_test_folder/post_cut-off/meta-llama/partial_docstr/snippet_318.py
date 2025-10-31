
from typing import Optional, Callable, Any, List, Dict


class PluginAPI:

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager', app_context: Optional['AppContext']):
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context

    @property
    def app_context(self) -> 'AppContext':
        if self._app_context is None:
            raise RuntimeError("Application context has not been set")
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        # Assuming that the PluginManager has a method to get API functions
        api_func = self._plugin_manager.get_api_function(name)
        if api_func is None:
            raise AttributeError(f"API function '{name}' not found")
        return api_func

    def list_available_apis(self) -> List[Dict[str, Any]]:
        return self._plugin_manager.list_available_apis()

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        self._plugin_manager.register_event_listener(
            event_name, self._plugin_name, callback)

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        self._plugin_manager.trigger_event(
            event_name, self._plugin_name, *args, **kwargs)

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        return self._plugin_manager.get_plugin_html_pages()

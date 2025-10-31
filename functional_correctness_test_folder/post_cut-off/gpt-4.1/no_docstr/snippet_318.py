
from typing import Optional, Callable, Any, List, Dict


class PluginAPI:

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager', app_context: Optional['AppContext']):
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context
        self._event_callbacks = {}  # event_name -> list of callbacks

    @property
    def app_context(self) -> 'AppContext':
        if self._app_context is None:
            raise RuntimeError(
                "AppContext has not been set on this PluginAPI instance.")
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        # Try to get an API method from the plugin manager's registry
        api_method = self._plugin_manager.get_api_method(name)
        if api_method is not None:
            return api_method
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def list_available_apis(self) -> List[Dict[str, Any]]:
        # Ask the plugin manager for all available APIs
        return self._plugin_manager.list_available_apis()

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        # Register a callback for a given event
        if event_name not in self._event_callbacks:
            self._event_callbacks[event_name] = []
        self._event_callbacks[event_name].append(callback)
        # Also register with the plugin manager's event system if needed
        self._plugin_manager.register_event_listener(
            event_name, self._plugin_name, callback)

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        # Send an event through the plugin manager's event system
        self._plugin_manager.send_event(event_name, *args, **kwargs)

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        # Ask the plugin manager for this plugin's HTML pages
        return self._plugin_manager.get_plugin_html_pages(self._plugin_name)

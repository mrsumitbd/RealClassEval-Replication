
from typing import Optional, Callable, Any, List, Dict


class PluginAPI:

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager', app_context: Optional['AppContext']):
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context

    @property
    def app_context(self) -> 'AppContext':
        if self._app_context is None:
            raise RuntimeError(
                "Application context has not been set on this PluginAPI instance.")
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        if name in self._plugin_manager._registered_apis:
            return self._plugin_manager._registered_apis[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def list_available_apis(self) -> List[Dict[str, Any]]:
        return self._plugin_manager.list_registered_apis()

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        self._plugin_manager.register_event_listener(
            event_name, self._plugin_name, callback)

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        self._plugin_manager.dispatch_event(
            event_name, self._plugin_name, *args, **kwargs)

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        return self._plugin_manager.get_html_pages_for_plugin(self._plugin_name)

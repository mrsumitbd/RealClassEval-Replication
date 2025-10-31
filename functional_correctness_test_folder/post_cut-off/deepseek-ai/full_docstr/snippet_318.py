
from typing import Any, Callable, List, Dict, Optional
from functools import partial


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
        if name in self._plugin_manager._api_registry:
            func = self._plugin_manager._api_registry[name]
            if hasattr(func, '__annotations__') and 'app_context' in func.__annotations__:
                return partial(func, app_context=self.app_context)
            return func
        raise AttributeError(f"API function '{name}' is not registered.")

    def list_available_apis(self) -> List[Dict[str, Any]]:
        apis = []
        for name, func in self._plugin_manager._api_registry.items():
            apis.append({
                'name': name,
                'parameters': list(func.__annotations__.items()) if hasattr(func, '__annotations__') else [],
                'doc': func.__doc__ or ''
            })
        return apis

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        self._plugin_manager.register_event_listener(
            self._plugin_name, event_name, callback)

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        kwargs['_triggering_plugin'] = self._plugin_name
        self._plugin_manager.dispatch_event(event_name, *args, **kwargs)

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        return self._plugin_manager.get_plugin_html_pages(self._plugin_name)

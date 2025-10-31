
import inspect
from functools import partial
from typing import Any, Callable, Dict, List, Optional


class PluginAPI:
    """
    Provides a safe, dynamic, and decoupled interface for plugins to access core APIs.
    """

    # Registry of core API functions that plugins can call.
    _api_registry: Dict[str, Callable[..., Any]] = {}

    @classmethod
    def register_api(cls, name: str, func: Callable[..., Any]) -> None:
        """
        Register a core API function that plugins can access via `self.api.<name>()`.
        """
        cls._api_registry[name] = func

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager',
                 app_context: Optional['AppContext']):
        """
        Initializes the PluginAPI instance for a specific plugin.
        """
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context

    @property
    def app_context(self) -> 'AppContext':
        """
        Provides direct access to the application's context.
        """
        if self._app_context is None:
            raise RuntimeError(
                f"AppContext not set for plugin '{self._plugin_name}'. "
                "This indicates an improper initialization sequence."
            )
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """
        Dynamically retrieves a registered core API function when accessed as an attribute.
        """
        if name not in self._api_registry:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'. "
                "This API function is not registered."
            )
        func = self._api_registry[name]
        sig = inspect.signature(func)
        if 'app_context' in sig.parameters:
            return partial(func, app_context=self.app_context)
        return func

    def list_available_apis(self) -> List[Dict[str, Any]]:
        """
        Returns a detailed list of all registered API functions.
        """
        apis = []
        for name, func in self._api_registry.items():
            sig = inspect.signature(func)
            params = [
                {
                    'name': p.name,
                    'annotation': p.annotation,
                    'default': p.default if p.default is not inspect._empty else None,
                }
                for p in sig.parameters.values()
            ]
            apis.append(
                {
                    'name': name,
                    'parameters': params,
                    'doc': inspect.getdoc(func) or '',
                }
            )
        return apis

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        """
        Registers a callback to be executed when a specific custom plugin event occurs.
        """
        def _wrapper(*args: Any, **kwargs: Any) -> None:
            kwargs['_triggering_plugin'] = self._plugin_name
            callback(*args, **kwargs)

        self._plugin_manager.register_event_listener(event_name, _wrapper)

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        """
        Triggers a custom plugin event, notifying all registered listeners.
        """
        self._plugin_manager.send_event(event_name, *args, **kwargs)

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        """
        Retrieves a list of plugin routes that are tagged for HTML rendering.
        """
        # The PluginManager is expected to expose a method that returns
        # the HTML routes for all plugins. If it does not exist, we return an empty list.
        if hasattr(self._plugin_manager, 'get_plugin_html_routes'):
            return self._plugin_manager.get_plugin_html_routes()
        return []

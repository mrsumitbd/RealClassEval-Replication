
from typing import Any, Callable, Dict, List, Optional
import inspect
from functools import partial


class PluginAPI:
    '''Provides a safe, dynamic, and decoupled interface for plugins to access core APIs.
    An instance of this class is passed to each plugin upon its initialization
    by the `PluginManager`. Plugins use this instance (typically `self.api`)
    to call registered core functions (e.g., `self.api.start_server(...)`)
    without needing to import them directly, thus avoiding circular dependencies
    and promoting a cleaner architecture.
    This class also provides methods for plugins to interact with the custom
    plugin event system, allowing them to listen for and send events to
    other plugins.
    '''

    # This registry is typically set by the PluginManager at startup.
    _api_registry: Dict[str, Callable[..., Any]] = {}

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager', app_context: Optional['AppContext']):
        '''Initializes the PluginAPI instance for a specific plugin.'''
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context

    @property
    def app_context(self) -> 'AppContext':
        '''Provides direct access to the application's context.'''
        if self._app_context is None:
            raise RuntimeError(
                "AppContext has not been set on this PluginAPI instance yet.")
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        '''Dynamically retrieves a registered core API function when accessed as an attribute.'''
        registry = type(self)._api_registry
        if name not in registry:
            raise AttributeError(
                f"API function '{name}' is not registered or unavailable.")
        func = registry[name]
        sig = inspect.signature(func)
        params = sig.parameters
        if 'app_context' in params:
            # Bind app_context as a keyword argument
            return partial(func, app_context=self._app_context)
        return func

    def list_available_apis(self) -> List[Dict[str, Any]]:
        '''
        Returns a detailed list of all registered API functions, including
        their names, parameters, and documentation.
        '''
        apis = []
        for name, func in type(self)._api_registry.items():
            sig = inspect.signature(func)
            doc = inspect.getdoc(func) or ""
            apis.append({
                'name': name,
                'parameters': [
                    {
                        'name': param_name,
                        'kind': str(param.kind),
                        'default': param.default if param.default is not inspect.Parameter.empty else None,
                        'annotation': str(param.annotation) if param.annotation is not inspect.Parameter.empty else None
                    }
                    for param_name, param in sig.parameters.items()
                ],
                'doc': doc
            })
        return apis

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        '''Registers a callback to be executed when a specific custom plugin event occurs.'''
        self._plugin_manager.register_event_listener(
            event_name, callback, self._plugin_name)

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        '''Triggers a custom plugin event, notifying all registered listeners.'''
        self._plugin_manager.dispatch_event(
            event_name, *args, _triggering_plugin=self._plugin_name, **kwargs)

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        '''
        Retrieves a list of plugin routes that are tagged for HTML rendering.
        '''
        if hasattr(self._plugin_manager, "get_plugin_html_pages"):
            return self._plugin_manager.get_plugin_html_pages(self._plugin_name)
        return []

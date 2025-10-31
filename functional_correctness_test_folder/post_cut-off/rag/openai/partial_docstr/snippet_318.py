
from __future__ import annotations

import inspect
import functools
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
)

# Forward references for type checking
try:
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from .plugin_manager import PluginManager  # noqa: F401
        from .app_context import AppContext  # noqa: F401
except Exception:
    # In case the imports are not available during runtime (e.g. circular imports),
    # we simply ignore them – the annotations will be resolved lazily.
    pass


class PluginAPI:
    """
    Provides a safe, dynamic, and decoupled interface for plugins to access core APIs.
    """

    # Registry of core API functions that plugins can call.
    _api_registry: Dict[str, Callable[..., Any]] = {}

    @classmethod
    def register_api(cls, name: str, func: Callable[..., Any]) -> None:
        """
        Register a core API function that plugins can access via the API bridge.
        """
        cls._api_registry[name] = func

    def __init__(
        self,
        plugin_name: str,
        plugin_manager: "PluginManager",
        app_context: Optional["AppContext"],
    ) -> None:
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context

    @property
    def app_context(self) -> "AppContext":
        """
        Provides direct access to the application's context.
        """
        if self._app_context is None:
            raise RuntimeError(
                f"PluginAPI for '{self._plugin_name}' has no AppContext set."
            )
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """
        Dynamically retrieves a registered core API function when accessed as an attribute.
        """
        if name not in self._api_registry:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'. "
                f"Available APIs: {list(self._api_registry)}"
            )

        func = self._api_registry[name]
        sig = inspect.signature(func)
        if "app_context" in sig.parameters:
            # Bind the app_context argument automatically
            return functools.partial(func, app_context=self.app_context)
        return func

    def list_available_apis(self) -> List[Dict[str, Any]]:
        """
        Returns a detailed list of all registered API functions.
        """
        apis: List[Dict[str, Any]] = []
        for name, func in self._api_registry.items():
            sig = inspect.signature(func)
            params = [
                {
                    "name": p.name,
                    "annotation": p.annotation,
                    "default": p.default
                    if p.default is not inspect._empty
                    else None,
                }
                for p in sig.parameters.values()
            ]
            apis.append(
                {
                    "name": name,
                    "parameters": params,
                    "doc": inspect.getdoc(func),
                }
            )
        return apis

    def listen_for_event(self, event_name: str, callback: Callable[..., None]) -> None:
        """
        Registers a callback to be executed when a specific custom plugin event occurs.
        """
        self._plugin_manager.register_event_listener(event_name, callback)

    def send_event(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        """
        Triggers a custom plugin event, notifying all registered listeners.
        """
        self._plugin_manager.send_event(event_name, *args, **kwargs)

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        """
        Retrieves a list of plugin routes that are tagged for HTML rendering.
        """
        # The PluginManager is expected to expose a method that returns
        # the routes for all plugins. If it does not exist, we return an empty list.
        try:
            return self._plugin_manager.get_plugin_html_routes()
        except AttributeError:
            return []

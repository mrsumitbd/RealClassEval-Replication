
from __future__ import annotations

import inspect
import functools
from typing import Any, Callable, Dict, List, Optional, Tuple

# Forward references for type checking only
# (The actual classes are defined elsewhere in the application)
# PluginManager and AppContext are expected to provide the following
# minimal interface for this implementation to work:
#
#   PluginManager:
#       api_registry: Dict[str, Callable[..., Any]]
#       register_event_listener(plugin_name: str, event_name: str,
#                               callback: Callable[..., None]) -> None
#       dispatch_event(event_name: str, *args: Any, **kwargs: Any) -> None
#       get_plugin_html_pages() -> List[Dict[str, str]]
#
#   AppContext:
#       (any attributes that plugins may access, e.g. settings, manager, etc.)


class PluginAPI:
    """Provides a safe, dynamic, and decoupled interface for plugins to access core APIs."""

    def __init__(
        self,
        plugin_name: str,
        plugin_manager: "PluginManager",
        app_context: Optional["AppContext"],
    ):
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context

        # The registry of core API functions is expected to be supplied by the
        # PluginManager.  If it is not present, we fall back to an empty dict.
        self._api_registry: Dict[str, Callable[..., Any]] = getattr(
            plugin_manager, "api_registry", {}
        )

    @property
    def app_context(self) -> "AppContext":
        """Provides direct access to the application's context."""
        if self._app_context is None:
            raise RuntimeError(
                f"PluginAPI for '{self._plugin_name}' has no AppContext set."
            )
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Dynamically retrieve a registered core API function."""
        if name not in self._api_registry:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'. "
                f"Available APIs: {list(self._api_registry)}"
            )

        func = self._api_registry[name]
        sig = inspect.signature(func)

        # If the function expects an `app_context` parameter, bind it automatically.
        if "app_context" in sig.parameters:
            return functools.partial(func, app_context=self.app_context)
        return func

    def list_available_apis(self) -> List[Dict[str, Any]]:
        """Return a detailed list of all registered API functions."""
        apis: List[Dict[str, Any]] = []
        for name, func in self._api_registry.items():
            sig = inspect.signature(func)
            params = [
                {
                    "name": p.name,
                    "annotation": p.annotation,
                    "default": p.default
                    if p.default is not inspect.Parameter.empty
                    else None,
                }
                for p in sig.parameters.values()
            ]
            apis.append(
                {
                    "name": name,
                    "parameters": params,
                    "doc": inspect.getdoc(func) or "",
                }
            )
        return apis

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        """Register a callback for a custom plugin event."""
        # Delegate to the PluginManager.  The manager is responsible for
        # storing the listener and invoking it when the event is fired.
        register = getattr(
            self._plugin_manager,
            "register_event_listener",
            None,
        )
        if register is None:
            raise AttributeError(
                "PluginManager does not provide 'register_event_listener' method."
            )
        register(self._plugin_name, event_name, callback)

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        """Trigger a custom plugin event."""
        dispatch = getattr(
            self._plugin_manager,
            "dispatch_event",
            None,
        )
        if dispatch is None:
            raise AttributeError(
                "PluginManager does not provide 'dispatch_event' method."
            )
        dispatch(event_name, *args, **kwargs)

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        """Retrieve a list of plugin routes tagged for HTML rendering."""
        getter = getattr(
            self._plugin_manager,
            "get_plugin_html_pages",
            None,
        )
        if getter is None:
            raise AttributeError(
                "PluginManager does not provide 'get_plugin_html_pages' method."
            )
        return getter()


from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple, get_type_hints
import inspect
import logging

log = logging.getLogger(__name__)


class PluginAPI:
    """
    Provides a public API for plugins to interact with the application
    and with other plugins.
    """

    def __init__(
        self,
        plugin_name: str,
        plugin_manager: "PluginManager",
        app_context: Optional["AppContext"],
    ):
        """
        Initializes the PluginAPI instance for a specific plugin.
        This constructor is called by the `PluginManager` when a plugin is
        being loaded and instantiated.
        Args:
            plugin_name (str): The name of the plugin for which this API
                instance is being created. This is used for logging and context.
            plugin_manager (PluginManager): A reference to the `PluginManager`
                instance. This is used to delegate custom event operations
                (listening and sending) to the manager.
            app_context (Optional[AppContext]): A reference to the global
                application context, providing access to shared application state
                and managers. This can be `None` during initial setup phases.
        """
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context

    @property
    def app_context(self) -> "AppContext":
        """
        Provides direct access to the application's context.
        This property returns the central `AppContext` object, which holds
        instances of key application components like the `Settings` manager,
        the `BedrockServerManager`, and the `PluginManager` itself.
        Example:

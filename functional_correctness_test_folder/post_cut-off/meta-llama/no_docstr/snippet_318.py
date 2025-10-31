
from typing import Optional, Callable, Any, List, Dict


class PluginAPI:

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager', app_context: Optional['AppContext']):
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context

    @property
    def app_context(self) -> 'AppContext':
        '''Provides direct access to the application's context.
        This property returns the central `AppContext` object, which holds
        instances of key application components like the `Settings` manager,
        the `BedrockServerManager`, and the `PluginManager` itself.
        Example:

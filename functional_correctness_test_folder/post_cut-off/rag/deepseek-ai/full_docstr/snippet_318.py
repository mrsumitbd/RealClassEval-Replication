
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

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager', app_context: Optional['AppContext']):
        '''Initializes the PluginAPI instance for a specific plugin.
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
        '''
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

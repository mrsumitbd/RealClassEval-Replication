import functools
import inspect
from typing import Dict, Any, Callable, TYPE_CHECKING, TypeVar, List
from typing import Optional

class PluginAPI:
    """Provides a safe, dynamic, and decoupled interface for plugins to access core APIs.

    An instance of this class is passed to each plugin upon its initialization
    by the `PluginManager`. Plugins use this instance (typically `self.api`)
    to call registered core functions (e.g., `self.api.start_server(...)`)
    without needing to import them directly, thus avoiding circular dependencies
    and promoting a cleaner architecture.

    This class also provides methods for plugins to interact with the custom
    plugin event system, allowing them to listen for and send events to
    other plugins.
    """

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager', app_context: Optional['AppContext']):
        """Initializes the PluginAPI instance for a specific plugin.

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
        self._plugin_name: str = plugin_name
        self._plugin_manager: 'PluginManager' = plugin_manager
        self._app_context: Optional['AppContext'] = app_context
        logger.debug(f"PluginAPI instance created for plugin '{self._plugin_name}'.")

    @property
    def app_context(self) -> 'AppContext':
        """Provides direct access to the application's context.

        This property returns the central `AppContext` object, which holds
        instances of key application components like the `Settings` manager,
        the `BedrockServerManager`, and the `PluginManager` itself.

        Example:
            ```python
            # In a plugin method:
            settings = self.api.app_context.settings
            server_manager = self.api.app_context.manager
            all_servers = server_manager.get_all_servers()
            ```

        Returns:
            AppContext: The application context instance.

        Raises:
            RuntimeError: If the application context has not been set on this
                `PluginAPI` instance yet. This would indicate an improper
                initialization sequence in the application startup.
        """
        if self._app_context is None:
            logger.critical(f"Plugin '{self._plugin_name}' tried to access `api.app_context`, but it has not been set. This indicates a critical error in the application's startup sequence.")
            raise RuntimeError('Application context is not available. It may not have been properly initialized and set for the PluginAPI.')
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Dynamically retrieves a registered core API function when accessed as an attribute.

        This magic method is the cornerstone of the API bridge's functionality.
        When a plugin executes code like `self.api.some_function_name()`, Python
        internally calls this `__getattr__` method with `name` set to
        `'some_function_name'`. This method then looks up `name` in the
        `_api_registry`.

        It also inspects the signature of the retrieved function. If the function
        has a parameter named `app_context`, this method automatically provides
        the `AppContext` to it, simplifying the function's implementation for
        both the core API and the plugin calling it.

        Args:
            name (str): The name of the attribute (API function) being accessed
                by the plugin.

        Returns:
            Callable[..., Any]: The callable API function retrieved from the
            `_api_registry` corresponding to the given `name`. If the function
            expects an `app_context`, a partial function with the context already
            bound is returned.

        Raises:
            AttributeError: If the function `name` has not been registered in
                the `_api_registry`, indicating the plugin is trying to access
                a non-existent or unavailable API function.
        """
        if name not in _api_registry:
            logger.error(f"Plugin '{self._plugin_name}' attempted to access unregistered API function: '{name}'.")
            raise AttributeError(f"The API function '{name}' has not been registered or does not exist. Available APIs: {list(_api_registry.keys())}")
        api_function = _api_registry[name]
        try:
            sig = inspect.signature(api_function)
            if 'app_context' in sig.parameters:
                logger.debug(f"API function '{name}' expects 'app_context'. Injecting it automatically.")
                return functools.partial(api_function, app_context=self.app_context)
        except (ValueError, TypeError) as e:
            logger.warning(f"Could not inspect the signature of API function '{name}'. Automatic 'app_context' injection will not be available for it. Error: {e}")
        logger.debug(f"Plugin '{self._plugin_name}' successfully accessed API function: '{name}'.")
        return api_function

    def list_available_apis(self) -> List[Dict[str, Any]]:
        """
        Returns a detailed list of all registered API functions, including
        their names, parameters, and documentation.

        This method can be useful for plugins that need to introspect the
        available core functionalities at runtime, or for debugging purposes
        to verify which APIs are exposed and how to call them.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, where each dictionary
            describes a registered API function.
        """
        import inspect
        api_details = []
        logger.debug(f"Plugin '{self._plugin_name}' requested detailed list of available APIs.")
        for name, func in sorted(_api_registry.items()):
            try:
                sig = inspect.signature(func)
                params_info = []
                for param in sig.parameters.values():
                    param_info = {'name': param.name, 'type_obj': param.annotation, 'default': param.default if param.default != inspect.Parameter.empty else 'REQUIRED'}
                    params_info.append(param_info)
                doc = inspect.getdoc(func)
                summary = doc.strip().split('\n')[0] if doc else 'No documentation available.'
                api_details.append({'name': name, 'parameters': params_info, 'docstring': summary})
            except (ValueError, TypeError) as e:
                logger.warning(f"Could not inspect signature for API '{name}': {e}")
                api_details.append({'name': name, 'parameters': [{'name': 'unknown', 'type': 'Any', 'default': 'unknown'}], 'docstring': 'Could not inspect function signature.'})
        return api_details

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        """Registers a callback to be executed when a specific custom plugin event occurs.

        This method allows a plugin to subscribe to custom events that may be
        triggered by other plugins via `send_event()`. The `PluginManager`
        handles the actual registration and dispatch of these events.

        Args:
            event_name (str): The unique name of the custom event to listen for
                (e.g., "myplugin:my_custom_event"). It is a recommended practice
                to namespace event names with the originating plugin's name or
                a unique prefix to avoid collisions.
            callback (Callable[..., None]): The function or method within the
                listening plugin that should be called when the specified event
                is triggered. This callback will receive any `*args` and
                `**kwargs` passed during the `send_event` call, plus an
                additional `_triggering_plugin` keyword argument (str)
                indicating the name of the plugin that sent the event.
        """
        logger.debug(f"Plugin '{self._plugin_name}' is attempting to register a listener for custom event '{event_name}' with callback '{callback.__name__}'.")
        self._plugin_manager.register_plugin_event_listener(event_name, callback, self._plugin_name)

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        """Triggers a custom plugin event, notifying all registered listeners.

        This method allows a plugin to broadcast a custom event to other plugins
        that have registered a listener for it using `listen_for_event()`.
        The `PluginManager` handles the dispatch of this event to all
        subscribed callbacks.

        Args:
            event_name (str): The unique name of the custom event to trigger.
                This should match the `event_name` used by listening plugins.
            *args (Any): Positional arguments to pass to the event listeners'
                callback functions.
            **kwargs (Any): Keyword arguments to pass to the event listeners'
                callback functions.
        """
        logger.debug(f"Plugin '{self._plugin_name}' is attempting to send custom event '{event_name}' with args: {args}, kwargs: {kwargs}.")
        self._plugin_manager.trigger_custom_plugin_event(event_name, self._plugin_name, *args, **kwargs)

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        """
        Retrieves a list of plugin routes that are tagged for HTML rendering.

        This allows the main application (or other plugins, if appropriate)
        to discover web pages provided by plugins that are intended to be
        directly accessible or linked in a UI.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, where each dictionary
            contains 'name' and 'path' for a route tagged for HTML rendering.
            The 'name' is a user-friendly display name for the link, and 'path'
            is the URL path for the route.
        """
        logger.debug(f"Plugin '{self._plugin_name}' (or core app via API) is requesting the list of HTML rendering plugin pages.")
        return self._plugin_manager.get_html_render_routes()

class ObservabilityManager:
    '''
    Manages observability callbacks for MCP agents.
    This class provides a centralized way to collect and manage callbacks
    from various observability platforms (Langfuse, Laminar, etc.).
    '''

    def __init__(self, custom_callbacks: list | None = None):
        '''
        Initialize the ObservabilityManager.
        Args:
            custom_callbacks: Optional list of custom callbacks to use instead of defaults.
        '''
        self.custom_callbacks = custom_callbacks if custom_callbacks is not None else []
        self.available_handlers = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        # For demonstration purposes, assume we have the following handlers
        # In a real implementation, you would dynamically collect available handlers
        self.available_handlers = ["Langfuse", "Laminar"]

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        if self.custom_callbacks:
            return self.custom_callbacks
        else:
            # For demonstration purposes, assume we have a function to get callbacks from handler names
            # In a real implementation, you would implement this logic
            return [self._get_callback_from_handler_name(handler) for handler in self.available_handlers]

    def _get_callback_from_handler_name(self, handler_name: str):
        # For demonstration purposes, assume we have a dictionary mapping handler names to callbacks
        # In a real implementation, you would implement this logic
        callbacks = {
            "Langfuse": lambda: print("Langfuse callback"),
            "Laminar": lambda: print("Laminar callback")
        }
        return callbacks.get(handler_name)

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        return self.available_handlers

    def has_callbacks(self) -> bool:
        '''
        Check if any callbacks are available.
        Returns:
            True if callbacks are available, False otherwise.
        '''
        return bool(self.get_callbacks())

    def add_callback(self, callback) -> None:
        '''
        Add a callback to the custom callbacks list.
        Args:
            callback: The callback to add.
        '''
        self.custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        '''Clear all custom callbacks.'''
        self.custom_callbacks = []

    def __repr__(self) -> str:
        '''String representation of the ObservabilityManager.'''
        return f"ObservabilityManager(custom_callbacks={self.custom_callbacks}, available_handlers={self.available_handlers})"

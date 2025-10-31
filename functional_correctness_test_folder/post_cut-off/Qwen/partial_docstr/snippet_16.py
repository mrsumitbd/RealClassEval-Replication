
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
        self.available_handlers = {}
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        # Example of collecting handlers, this should be replaced with actual logic
        self.available_handlers = {
            "Langfuse": lambda x: print(f"Langfuse handling {x}"),
            "Laminar": lambda x: print(f"Laminar handling {x}")
        }

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        return self.custom_callbacks if self.custom_callbacks else list(self.available_handlers.values())

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        return list(self.available_handlers.keys())

    def has_callbacks(self) -> bool:
        return bool(self.custom_callbacks) or bool(self.available_handlers)

    def add_callback(self, callback) -> None:
        '''
        Add a callback to the custom callbacks list.
        Args:
            callback: The callback to add.
        '''
        self.custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        '''Clear all custom callbacks.'''
        self.custom_callbacks.clear()

    def __repr__(self) -> str:
        '''String representation of the ObservabilityManager.'''
        return f"ObservabilityManager(custom_callbacks={self.custom_callbacks}, available_handlers={list(self.available_handlers.keys())})"

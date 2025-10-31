
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
        self._custom_callbacks = custom_callbacks
        self._available_handlers = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        self._available_handlers = []
        try:
            import langfuse
            self._available_handlers.append(langfuse.callback)
        except ImportError:
            pass
        try:
            import laminar
            self._available_handlers.append(laminar.callback)
        except ImportError:
            pass

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        if self._custom_callbacks is not None:
            return self._custom_callbacks
        return self._available_handlers

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        names = []
        for handler in self._available_handlers:
            if 'langfuse' in str(handler.__module__).lower():
                names.append("Langfuse")
            elif 'laminar' in str(handler.__module__).lower():
                names.append("Laminar")
        return names

    def has_callbacks(self) -> bool:
        '''
        Check if any callbacks are available.
        Returns:
            True if callbacks are available, False otherwise.
        '''
        return len(self.get_callbacks()) > 0

    def add_callback(self, callback) -> None:
        '''
        Add a callback to the custom callbacks list.
        Args:
            callback: The callback to add.
        '''
        if self._custom_callbacks is None:
            self._custom_callbacks = []
        self._custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        '''Clear all custom callbacks.'''
        self._custom_callbacks = None

    def __repr__(self) -> str:
        '''String representation of the ObservabilityManager.'''
        return f"ObservabilityManager(custom_callbacks={self._custom_callbacks}, available_handlers={self.get_handler_names()})"

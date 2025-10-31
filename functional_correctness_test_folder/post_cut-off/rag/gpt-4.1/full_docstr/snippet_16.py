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
        self._custom_callbacks = list(
            custom_callbacks) if custom_callbacks is not None else None
        self._available_handlers = []
        self._handler_names = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        self._available_handlers = []
        self._handler_names = []

        # Try to import and instantiate known observability handlers
        # Add more handlers here as needed
        try:
            from langfuse.callback import LangfuseCallbackHandler
            self._available_handlers.append(LangfuseCallbackHandler())
            self._handler_names.append("Langfuse")
        except Exception:
            pass

        try:
            from laminar.callback import LaminarCallbackHandler
            self._available_handlers.append(LaminarCallbackHandler())
            self._handler_names.append("Laminar")
        except Exception:
            pass

        # Add more handlers here as needed

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
        if self._custom_callbacks is not None:
            # Try to get names from custom callbacks if possible
            names = []
            for cb in self._custom_callbacks:
                name = getattr(cb, "__class__", type(cb)).__name__
                names.append(name)
            return names
        return self._handler_names

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
        if self._custom_callbacks is None:
            self._custom_callbacks = []
        self._custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        '''Clear all custom callbacks.'''
        self._custom_callbacks = []

    def __repr__(self) -> str:
        '''String representation of the ObservabilityManager.'''
        cb_names = self.get_handler_names()
        return f"<ObservabilityManager callbacks={cb_names!r}>"

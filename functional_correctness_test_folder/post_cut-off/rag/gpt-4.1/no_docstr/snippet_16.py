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
        self._custom_callbacks = custom_callbacks[:
                                                  ] if custom_callbacks is not None else None
        self._available_handlers = []
        self._handler_names = []
        self._collected = False

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        # This is a placeholder for actual handler collection logic.
        # In a real implementation, this would import and instantiate handlers from available platforms.
        # For demonstration, we simulate two handlers.
        class LangfuseHandler:
            def __call__(self, *args, **kwargs): pass
            def __repr__(self): return "<LangfuseHandler>"

        class LaminarHandler:
            def __call__(self, *args, **kwargs): pass
            def __repr__(self): return "<LaminarHandler>"

        self._available_handlers = [LangfuseHandler(), LaminarHandler()]
        self._handler_names = ["Langfuse", "Laminar"]
        self._collected = True

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        if self._custom_callbacks is not None:
            return self._custom_callbacks
        if not self._collected:
            self._collect_available_handlers()
        return self._available_handlers

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        if not self._collected:
            self._collect_available_handlers()
        return self._handler_names

    def has_callbacks(self) -> bool:
        '''
        Check if any callbacks are available.
        Returns:
            True if callbacks are available, False otherwise.
        '''
        callbacks = self.get_callbacks()
        return bool(callbacks)

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
        if self._custom_callbacks is not None:
            cb_names = [getattr(cb, '__name__', repr(cb))
                        for cb in self._custom_callbacks]
            return f"<ObservabilityManager custom_callbacks={cb_names}>"
        else:
            names = self.get_handler_names()
            return f"<ObservabilityManager available_handlers={names}>"

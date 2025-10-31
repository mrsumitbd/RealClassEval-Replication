
class ObservabilityManager:
    '''
    Manages observability callbacks for MCP agents.
    This class provides a centralized way to collect and manage callbacks
    from various observability platforms (Langfuse, Laminar, etc.).
    '''
    # Simulated available handlers for demonstration
    _PLATFORM_HANDLERS = [
        {"name": "Langfuse", "callback": lambda *a, **kw: "Langfuse callback"},
        {"name": "Laminar", "callback": lambda *a, **kw: "Laminar callback"},
    ]

    def __init__(self, custom_callbacks: list | None = None):
        '''
        Initialize the ObservabilityManager.
        Args:
            custom_callbacks: Optional list of custom callbacks to use instead of defaults.
        '''
        self._custom_callbacks = custom_callbacks[:
                                                  ] if custom_callbacks is not None else None
        self._available_handlers = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        self._available_handlers = [handler["callback"]
                                    for handler in self._PLATFORM_HANDLERS]

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
        return [handler["name"] for handler in self._PLATFORM_HANDLERS]

    def has_callbacks(self) -> bool:
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
        if self._custom_callbacks is not None:
            cb_count = len(self._custom_callbacks)
            cb_type = "custom"
        else:
            cb_count = len(self._available_handlers)
            cb_type = "default"
        return f"<ObservabilityManager ({cb_type} callbacks: {cb_count})>"

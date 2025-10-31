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
        self._custom_callbacks: list = list(
            custom_callbacks) if custom_callbacks else []
        self._available_handlers: list = []
        self._available_handler_names: list[str] = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        # Placeholder for future auto-discovery of platform-specific handlers.
        # Intentionally conservative to avoid importing optional dependencies.
        self._available_handlers = []
        self._available_handler_names = []

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        if self._custom_callbacks:
            return list(self._custom_callbacks)
        return list(self._available_handlers)

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        callbacks = self.get_callbacks()
        names: list[str] = []
        for cb in callbacks:
            # Prefer explicit "name" attribute if available
            if hasattr(cb, "name"):
                try:
                    names.append(str(getattr(cb, "name")))
                    continue
                except Exception:
                    pass
            # Fall back to class or type name
            try:
                if hasattr(cb, "__class__"):
                    names.append(cb.__class__.__name__)
                else:
                    names.append(type(cb).__name__)
            except Exception:
                names.append("UnknownCallback")
        # If there are no current callbacks, return known available handler names
        if not names and self._available_handler_names:
            return list(self._available_handler_names)
        return names

    def has_callbacks(self) -> bool:
        return len(self.get_callbacks()) > 0

    def add_callback(self, callback) -> None:
        '''
        Add a callback to the custom callbacks list.
        Args:
            callback: The callback to add.
        '''
        if self._custom_callbacks is None:
            self._custom_callbacks = []
        if callback not in self._custom_callbacks:
            self._custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        '''Clear all custom callbacks.'''
        self._custom_callbacks = []

    def __repr__(self) -> str:
        names = self.get_handler_names()
        return f"ObservabilityManager(callback_count={len(self.get_callbacks())}, handlers={names})"

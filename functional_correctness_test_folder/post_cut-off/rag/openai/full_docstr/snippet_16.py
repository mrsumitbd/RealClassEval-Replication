
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
        # Store custom callbacks; if None, start with an empty list
        self.custom_callbacks: list = list(
            custom_callbacks) if custom_callbacks else []
        # List of available handlers discovered by _collect_available_handlers
        self._available_handlers: list = []
        # Discover available handlers (if any)
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        # In a real implementation this would discover installed
        # observability modules (e.g., Langfuse, Laminar, etc.).
        # For the purposes of this library we simply expose a
        # minimal set of placeholder handlers if the corresponding
        # modules can be imported.
        handlers = []

        # Attempt to import Langfuse handler
        try:
            from .langfuse_handler import LangfuseHandler  # type: ignore
            handlers.append(LangfuseHandler())
        except Exception:
            pass

        # Attempt to import Laminar handler
        try:
            from .laminar_handler import LaminarHandler  # type: ignore
            handlers.append(LaminarHandler())
        except Exception:
            pass

        # Store discovered handlers
        self._available_handlers = handlers

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        if self.custom_callbacks:
            return list(self.custom_callbacks)
        return list(self._available_handlers)

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        names = []
        for handler in self._available_handlers:
            # Prefer a `name` attribute if present, otherwise use class name
            names.append(getattr(handler, 'name', handler.__class__.__name__))
        return names

    def has_callbacks(self) -> bool:
        '''
        Check if any callbacks are available.
        Returns:
            True if callbacks are available, False otherwise.
        '''
        return bool(self.custom_callbacks or self._available_handlers)

    def add_callback(self, callback) -> None:
        '''
        Add a callback to the custom callbacks list.
        Args:
            callback: The callback to add.
        '''
        if callback not in self.custom_callbacks:
            self.custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        '''Clear all custom callbacks.'''
        self.custom_callbacks.clear()

    def __repr__(self) -> str:
        '''String representation of the ObservabilityManager.'''
        callbacks = self.get_callbacks()
        names = [getattr(cb, 'name', cb.__class__.__name__)
                 for cb in callbacks]
        return f"<ObservabilityManager callbacks={names}>"

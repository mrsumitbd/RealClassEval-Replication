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
        self._handler_names: list[str] = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        self._available_handlers = []
        self._handler_names = []

        # Try to discover Langfuse callback handler
        try:
            # Common official package
            from langfuse.callback import CallbackHandler as LangfuseCallbackHandler  # type: ignore
            try:
                handler = LangfuseCallbackHandler()  # try default constructor
                self._available_handlers.append(handler)
            except Exception:
                # Could not instantiate without args; skip silently
                pass
        except Exception:
            pass

        # Try to discover Laminar callback handler (best-effort; package APIs may vary)
        laminar_handler_candidates = [
            ("laminar", "CallbackHandler"),
            ("laminar.callback", "CallbackHandler"),
            ("laminar.observability", "CallbackHandler"),
            ("laminar", "ObservabilityCallback"),
        ]
        for module_name, attr_name in laminar_handler_candidates:
            try:
                module = __import__(module_name, fromlist=[attr_name])
                handler_cls = getattr(module, attr_name, None)
                if handler_cls is None:
                    continue
                try:
                    handler = handler_cls()
                    self._available_handlers.append(handler)
                    break
                except Exception:
                    # Could not instantiate; try next candidate
                    continue
            except Exception:
                continue

        # Build handler names
        self._handler_names = [self._callback_name(
            cb) for cb in self._available_handlers]

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        return self._custom_callbacks if self._custom_callbacks else list(self._available_handlers)

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        callbacks = self._custom_callbacks if self._custom_callbacks else self._available_handlers
        return [self._callback_name(cb) for cb in callbacks]

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
        self._custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        '''Clear all custom callbacks.'''
        self._custom_callbacks.clear()

    def __repr__(self) -> str:
        '''String representation of the ObservabilityManager.'''
        active = self.get_handler_names()
        return f"ObservabilityManager(callbacks={active})"

    @staticmethod
    def _callback_name(callback) -> str:
        # Prefer explicit 'name' attribute if available
        try:
            name = getattr(callback, "name", None)
            if isinstance(name, str) and name.strip():
                return name
        except Exception:
            pass
        # Fallback to class name
        try:
            return callback.__class__.__name__
        except Exception:
            return str(callback)

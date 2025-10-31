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
        if custom_callbacks is not None and not isinstance(custom_callbacks, list):
            raise TypeError("custom_callbacks must be a list or None")
        self._custom_callbacks = custom_callbacks
        self._available_callbacks: list = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        self._available_callbacks = []

        # Langfuse
        try:
            # Common import path used by langfuse python SDK for callback handler
            from langfuse.callback import CallbackHandler as LangfuseCallbackHandler  # type: ignore
            try:
                handler = LangfuseCallbackHandler()  # type: ignore
            except TypeError:
                # Some versions may require explicit args; skip if instantiation fails
                handler = None
            if handler is not None:
                self._available_callbacks.append(handler)
        except Exception:
            pass

        # Laminar (best-effort guessing of import paths)
        laminar_handler = None
        try:
            # Try a likely callback handler location
            from laminar.callbacks import CallbackHandler as LaminarCallbackHandler  # type: ignore
            try:
                laminar_handler = LaminarCallbackHandler()  # type: ignore
            except TypeError:
                laminar_handler = None
        except Exception:
            try:
                # Alternate guess
                from laminar import CallbackHandler as LaminarCallbackHandlerAlt  # type: ignore
                try:
                    laminar_handler = LaminarCallbackHandlerAlt()  # type: ignore
                except TypeError:
                    laminar_handler = None
            except Exception:
                laminar_handler = None
        if laminar_handler is not None:
            self._available_callbacks.append(laminar_handler)

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        if self._custom_callbacks is not None:
            return self._custom_callbacks
        return list(self._available_callbacks)

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        names: list[str] = []
        for cb in self.get_callbacks():
            name = None
            # Prefer an explicit 'name' attribute if present
            name = getattr(cb, 'name', None)
            if not isinstance(name, str) or not name:
                # Derive from module if possible
                mod = getattr(cb, '__module__', '')
                if isinstance(mod, str) and mod:
                    root = mod.split('.')[0]
                    if root:
                        name = root.capitalize()
                # Fallback to class name
                if not name:
                    if isinstance(cb, type):
                        name = cb.__name__
                    else:
                        name = cb.__class__.__name__
            names.append(str(name))
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
        names = self.get_handler_names()
        return f'ObservabilityManager(callbacks={names})'

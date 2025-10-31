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
        self._custom_callbacks_provided = custom_callbacks is not None
        self._custom_callbacks = list(
            custom_callbacks) if custom_callbacks is not None else None
        self._available_handlers: list = []
        self._available_handler_names: list[str] = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        self._available_handlers = []
        self._available_handler_names = []

        # Try to detect well-known observability callback handlers.
        # This is best-effort and safe if packages are not installed.
        import importlib

        attempted_modules = [
            # Langfuse
            "langfuse.callback",
            "langfuse",
            # Laminar (module name may vary, try common guesses)
            "laminar.callbacks",
            "laminar",
        ]

        attr_candidates = [
            # common handler names
            "LangfuseCallbackHandler",
            "LaminarCallbackHandler",
            "CallbackHandler",
            # factory-style names
            "get_callback_handler",
            "get_callback",
            "create_callback_handler",
            "handler",
            "callback_handler",
        ]

        added_names = set()

        for mod_name in attempted_modules:
            try:
                mod = importlib.import_module(mod_name)
            except Exception:
                continue

            # Derive a friendly display name from module
            if mod_name.startswith("langfuse"):
                display_name = "Langfuse"
            elif mod_name.startswith("laminar"):
                display_name = "Laminar"
            else:
                # Capitalize the top-level module name as a fallback
                display_name = mod_name.split(".")[0].capitalize()

            # Avoid duplicates if we already added a handler for this display name
            if display_name in added_names:
                continue

            handler_obj = None
            for attr in attr_candidates:
                if hasattr(mod, attr):
                    candidate = getattr(mod, attr)
                    try:
                        if callable(candidate):
                            # Try calling without args (common pattern)
                            obj = candidate()
                        else:
                            obj = candidate
                        # Ensure we have some object to use as callback
                        if obj is not None:
                            handler_obj = obj
                            break
                    except Exception:
                        # If instantiation fails, try next attribute
                        continue

            if handler_obj is not None:
                self._available_handlers.append(handler_obj)
                self._available_handler_names.append(display_name)
                added_names.add(display_name)

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        if self._custom_callbacks_provided:
            return self._custom_callbacks or []
        return list(self._available_handlers)

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        if self._custom_callbacks_provided:
            names = []
            for cb in (self._custom_callbacks or []):
                # Prefer explicit "name" attribute if provided; else function/class name
                name = getattr(cb, "name", None)
                if isinstance(name, str) and name:
                    names.append(name)
                    continue
                name = getattr(cb, "__name__", None)
                if isinstance(name, str) and name:
                    names.append(name)
                    continue
                names.append(cb.__class__.__name__)
            return names
        return list(self._available_handler_names)

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
        # Mark as custom-provided to ensure we use the custom set
        self._custom_callbacks_provided = True
        self._custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        '''Clear all custom callbacks.'''
        self._custom_callbacks = []
        # Keep _custom_callbacks_provided = True so that an explicit clear
        # results in using no callbacks, rather than falling back to defaults.

    def __repr__(self) -> str:
        '''String representation of the ObservabilityManager.'''
        mode = "custom" if self._custom_callbacks_provided else "auto"
        names = self.get_handler_names()
        return f"ObservabilityManager(mode={mode}, callbacks={names})"

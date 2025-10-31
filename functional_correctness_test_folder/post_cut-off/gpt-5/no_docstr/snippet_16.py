class ObservabilityManager:

    def __init__(self, custom_callbacks: list | None = None):
        if custom_callbacks is None:
            self._callbacks: list = []
        elif isinstance(custom_callbacks, list):
            self._callbacks = list(custom_callbacks)
        else:
            raise TypeError("custom_callbacks must be a list or None")
        self._handler_names: list[str] = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        handlers = set()
        for cb in self._callbacks:
            if callable(cb) and not hasattr(cb, "__self__") and not hasattr(cb, "__dict__"):
                name = getattr(cb, "__name__", None)
                if isinstance(name, str) and not name.startswith("_"):
                    handlers.add(name)
                continue
            for attr_name in dir(cb):
                if attr_name.startswith("_"):
                    continue
                try:
                    attr = getattr(cb, attr_name)
                except Exception:
                    continue
                if callable(attr):
                    handlers.add(attr_name)
        self._handler_names = sorted(handlers)

    def get_callbacks(self) -> list:
        return list(self._callbacks)

    def get_handler_names(self) -> list[str]:
        return list(self._handler_names)

    def has_callbacks(self) -> bool:
        return bool(self._callbacks)

    def add_callback(self, callback) -> None:
        self._callbacks.append(callback)
        self._collect_available_handlers()

    def clear_callbacks(self) -> None:
        self._callbacks.clear()
        self._handler_names.clear()

    def __repr__(self) -> str:
        return f"ObservabilityManager(callbacks={len(self._callbacks)}, handlers={self._handler_names})"

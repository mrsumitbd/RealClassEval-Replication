
class ObservabilityManager:

    def __init__(self, custom_callbacks: list | None = None):
        self._callbacks = []
        if custom_callbacks is not None:
            self._callbacks.extend(custom_callbacks)
        self._handlers = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        self._handlers = ["default_handler", "advanced_handler"]

    def get_callbacks(self) -> list:
        return self._callbacks.copy()

    def get_handler_names(self) -> list[str]:
        return self._handlers.copy()

    def has_callbacks(self) -> bool:
        return len(self._callbacks) > 0

    def add_callback(self, callback) -> None:
        self._callbacks.append(callback)

    def clear_callbacks(self) -> None:
        self._callbacks.clear()

    def __repr__(self) -> str:
        return f"ObservabilityManager(callbacks={len(self._callbacks)}, handlers={len(self._handlers)})"

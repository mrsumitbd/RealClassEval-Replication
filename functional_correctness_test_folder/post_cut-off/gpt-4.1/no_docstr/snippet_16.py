
class ObservabilityManager:

    def __init__(self, custom_callbacks: list | None = None):
        self._callbacks = list(
            custom_callbacks) if custom_callbacks is not None else []
        self._handlers = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        # For demonstration, let's assume some default handlers
        self._handlers = ['logging', 'metrics', 'tracing']

    def get_callbacks(self) -> list:
        return list(self._callbacks)

    def get_handler_names(self) -> list[str]:
        return list(self._handlers)

    def has_callbacks(self) -> bool:
        return len(self._callbacks) > 0

    def add_callback(self, callback) -> None:
        self._callbacks.append(callback)

    def clear_callbacks(self) -> None:
        self._callbacks.clear()

    def __repr__(self) -> str:
        return (f"ObservabilityManager(callbacks={len(self._callbacks)}, "
                f"handlers={self._handlers})")

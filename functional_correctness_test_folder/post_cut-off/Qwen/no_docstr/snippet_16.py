
class ObservabilityManager:

    def __init__(self, custom_callbacks: list | None = None):
        self.callbacks = custom_callbacks if custom_callbacks is not None else []

    def _collect_available_handlers(self) -> None:
        self.available_handlers = {
            callback.__name__: callback for callback in self.callbacks}

    def get_callbacks(self) -> list:
        return self.callbacks

    def get_handler_names(self) -> list[str]:
        return list(self.available_handlers.keys())

    def has_callbacks(self) -> bool:
        return len(self.callbacks) > 0

    def add_callback(self, callback) -> None:
        self.callbacks.append(callback)
        self._collect_available_handlers()

    def clear_callbacks(self) -> None:
        self.callbacks.clear()
        self._collect_available_handlers()

    def __repr__(self) -> str:
        return f"ObservabilityManager(callbacks={self.callbacks})"

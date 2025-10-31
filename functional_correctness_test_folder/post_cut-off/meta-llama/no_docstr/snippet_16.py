
class ObservabilityManager:

    def __init__(self, custom_callbacks: list | None = None):
        self._available_handlers = {}
        self._callbacks = []
        self._collect_available_handlers()
        if custom_callbacks is not None:
            for callback in custom_callbacks:
                self.add_callback(callback)

    def _collect_available_handlers(self) -> None:
        # For demonstration purposes, assume we have some handlers
        # In a real application, this could be dynamically loaded or registered
        self._available_handlers = {
            'handler1': 'Handler 1',
            'handler2': 'Handler 2',
            'handler3': 'Handler 3',
        }

    def get_callbacks(self) -> list:
        return self._callbacks

    def get_handler_names(self) -> list[str]:
        return list(self._available_handlers.keys())

    def has_callbacks(self) -> bool:
        return len(self._callbacks) > 0

    def add_callback(self, callback) -> None:
        if callable(callback):
            self._callbacks.append(callback)
        else:
            raise ValueError("Callback must be callable")

    def clear_callbacks(self) -> None:
        self._callbacks.clear()

    def __repr__(self) -> str:
        return f"ObservabilityManager(callbacks={self._callbacks}, available_handlers={self._available_handlers})"


# Example usage:
if __name__ == "__main__":
    def custom_callback():
        print("Custom callback executed")

    manager = ObservabilityManager([custom_callback])
    print(manager.get_handler_names())
    print(manager.has_callbacks())
    print(manager.get_callbacks())
    manager.clear_callbacks()
    print(manager.has_callbacks())
    print(manager)

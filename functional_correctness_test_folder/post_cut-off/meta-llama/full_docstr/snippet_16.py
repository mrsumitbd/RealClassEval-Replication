
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
        self.custom_callbacks = custom_callbacks if custom_callbacks is not None else []
        self.available_handlers = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        # For demonstration purposes, assume we have the following handlers
        # In a real-world scenario, this would be dynamically collected from configured platforms
        self.available_handlers = [
            {"name": "Langfuse", "callback": lambda: print(
                "Langfuse callback")},
            {"name": "Laminar", "callback": lambda: print("Laminar callback")},
        ]

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        if self.custom_callbacks:
            return self.custom_callbacks
        return [handler["callback"] for handler in self.available_handlers]

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        return [handler["name"] for handler in self.available_handlers]

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
        self.custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        '''Clear all custom callbacks.'''
        self.custom_callbacks.clear()

    def __repr__(self) -> str:
        '''String representation of the ObservabilityManager.'''
        return f"ObservabilityManager(custom_callbacks={self.custom_callbacks}, available_handlers={self.available_handlers})"


# Example usage:
if __name__ == "__main__":
    manager = ObservabilityManager()
    print(manager.get_handler_names())  # Output: ['Langfuse', 'Laminar']
    print(manager.has_callbacks())  # Output: True
    callbacks = manager.get_callbacks()
    for callback in callbacks:
        callback()  # Output: Langfuse callback, Laminar callback

    def custom_callback(): return print("Custom callback")
    manager.add_callback(custom_callback)
    print(manager.get_callbacks())  # Output: [<function __main__.<lambda>()>]
    manager.clear_callbacks()
    # Output: [<function __main__.<lambda>() at 0x...>, <function __main__.<lambda>() at 0x...>]
    print(manager.get_callbacks())
    # Output: ObservabilityManager(custom_callbacks=[], available_handlers=[{'name': 'Langfuse', 'callback': <function ObservabilityManager._collect_available_handlers.<locals>.<lambda> at 0x...>}, {'name': 'Laminar', 'callback': <function ObservabilityManager._collect_available_handlers.<locals>.<lambda> at 0x...>}])
    print(manager)

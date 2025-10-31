
class ObservabilityManager:
    """
    A simple manager for observability callbacks.

    The manager keeps a list of callbacks that can be invoked by external
    components.  It also keeps a list of *available* handlers that can be
    discovered automatically.  The default implementation does not discover
    any handlers – subclasses or users can override `_collect_available_handlers`
    to provide custom logic.
    """

    def __init__(self, custom_callbacks: list | None = None):
        """
        Initialize the manager.

        Parameters
        ----------
        custom_callbacks : list | None, optional
            A list of callbacks to start with.  If ``None`` an empty list is
            used.
        """
        self._callbacks: list = list(
            custom_callbacks) if custom_callbacks else []
        self._available_handlers: list = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        """
        Populate ``self._available_handlers`` with default handlers.

        The base implementation does nothing.  Subclasses may override this
        method to discover handlers automatically (e.g. by inspecting
        modules or using entry points).
        """
        # Default implementation: no handlers are automatically discovered.
        self._available_handlers = []

    def get_callbacks(self) -> list:
        """
        Return the list of registered callbacks.

        Returns
        -------
        list
            The current list of callbacks.
        """
        return list(self._callbacks)

    def get_handler_names(self) -> list[str]:
        """
        Return the names of all available handlers.

        Returns
        -------
        list[str]
            A list of handler names.
        """
        return [handler.__name__ for handler in self._available_handlers]

    def has_callbacks(self) -> bool:
        """
        Check whether any callbacks are registered.

        Returns
        -------
        bool
            ``True`` if at least one callback is registered, otherwise
            ``False``.
        """
        return bool(self._callbacks)

    def add_callback(self, callback) -> None:
        """
        Add a new callback to the manager.

        Parameters
        ----------
        callback
            A callable to be added to the callback list.
        """
        if not callable(callback):
            raise TypeError("callback must be callable")
        self._callbacks.append(callback)

    def clear_callbacks(self) -> None:
        """
        Remove all registered callbacks.
        """
        self._callbacks.clear()

    def __repr__(self) -> str:
        """
        Return a string representation of the manager.

        The representation includes the number of callbacks and the names of
        available handlers.
        """
        return (
            f"{self.__class__.__name__}("
            f"callbacks={len(self._callbacks)}, "
            f"available_handlers={self.get_handler_names()})"
        )

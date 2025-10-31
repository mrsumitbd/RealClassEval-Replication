
from __future__ import annotations
from typing import Callable, List, Optional, Any


class ObservabilityManager:
    """
    Manages observability callbacks for MCP agents.
    This class provides a centralized way to collect and manage callbacks
    from various observability platforms (Langfuse, Laminar, etc.).
    """

    def __init__(self, custom_callbacks: Optional[List[Callable]] = None):
        """
        Initialize the ObservabilityManager.

        Args:
            custom_callbacks: Optional list of custom callbacks to use instead of defaults.
        """
        self.custom_callbacks: List[Callable] = custom_callbacks or []
        self._available_handlers: List[Callable] = []
        self._handler_names: List[str] = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        """Collect all available observability handlers from configured platforms."""
        # Attempt to import Langfuse
        try:
            import langfuse  # type: ignore
            # Simple placeholder callback for Langfuse

            def langfuse_callback(*args: Any, **kwargs: Any) -> None:
                print("Langfuse callback invoked")
            self._available_handlers.append(langfuse_callback)
            self._handler_names.append("Langfuse")
        except Exception:
            pass

        # Attempt to import Laminar
        try:
            import laminar  # type: ignore
            # Simple placeholder callback for Laminar

            def laminar_callback(*args: Any, **kwargs: Any) -> None:
                print("Laminar callback invoked")
            self._available_handlers.append(laminar_callback)
            self._handler_names.append("Laminar")
        except Exception:
            pass

        # Add more platforms here as needed

    def get_callbacks(self) -> List[Callable]:
        """
        Get the list of callbacks to use.

        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        """
        if self.custom_callbacks:
            return self.custom_callbacks
        return self._available_handlers

    def get_handler_names(self) -> List[str]:
        """
        Get the names of available handlers.

        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        """
        return self._handler_names

    def has_callbacks(self) -> bool:
        """Return True if there are any callbacks to use."""
        return bool(self.get_callbacks())

    def add_callback(self, callback: Callable) -> None:
        """
        Add a callback to the custom callbacks list.

        Args:
            callback: The callback to add.
        """
        if callback not in self.custom_callbacks:
            self.custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        """Clear all custom callbacks."""
        self.custom_callbacks.clear()

    def __repr__(self) -> str:
        """String representation of the ObservabilityManager."""
        return (
            f"<ObservabilityManager "
            f"callbacks={len(self.get_callbacks())} "
            f"handlers={self.get_handler_names()}>"
        )

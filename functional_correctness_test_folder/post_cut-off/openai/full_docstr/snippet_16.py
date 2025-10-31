
import importlib.util
from typing import Callable, List, Optional


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
        self._available_handlers: dict[str, Callable] = {}
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        """Collect all available observability handlers from configured platforms."""
        # Langfuse
        if importlib.util.find_spec("langfuse"):
            try:
                import langfuse

                def langfuse_handler(event: dict) -> None:
                    # Example: send event to Langfuse
                    langfuse.trace(event)

                self._available_handlers["Langfuse"] = langfuse_handler
            except Exception:
                pass

        # Laminar
        if importlib.util.find_spec("laminar"):
            try:
                import laminar

                def laminar_handler(event: dict) -> None:
                    # Example: send event to Laminar
                    laminar.send(event)

                self._available_handlers["Laminar"] = laminar_handler
            except Exception:
                pass

        # Add more platforms here following the same pattern

    def get_callbacks(self) -> List[Callable]:
        """
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        """
        return self.custom_callbacks if self.custom_callbacks else list(
            self._available_handlers.values()
        )

    def get_handler_names(self) -> List[str]:
        """
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        """
        return list(self._available_handlers.keys())

    def has_callbacks(self) -> bool:
        """
        Check if any callbacks are available.
        Returns:
            True if callbacks are available, False otherwise.
        """
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
        names = self.get_handler_names()
        custom = len(self.custom_callbacks)
        return (
            f"<ObservabilityManager "
            f"custom_callbacks={custom} "
            f"available_handlers={names}>"
        )

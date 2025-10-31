
import os
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
        self._custom_callbacks: List[Callable] = list(
            custom_callbacks) if custom_callbacks else []
        self._available_handlers: List[Callable] = []
        self._handler_names: List[str] = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        """
        Collect all available observability handlers from configured platforms.
        The platforms are specified via the environment variable
        `OBSERVABILITY_HANDLERS` as a comma‑separated list of names.
        For each name a simple placeholder callback is created that
        prints a message when invoked.
        """
        env = os.getenv("OBSERVABILITY_HANDLERS", "")
        names = [name.strip() for name in env.split(",") if name.strip()]
        self._handler_names = names
        self._available_handlers = []

        for name in names:
            # Create a simple placeholder callback that logs its name.
            def make_callback(n: str) -> Callable:
                def callback(*args, **kwargs):
                    # The actual implementation would forward data to the
                    # observability platform. Here we just log for debugging.
                    print(f"[{n} callback] args={args} kwargs={kwargs}")
                return callback

            self._available_handlers.append(make_callback(name))

    def get_callbacks(self) -> List[Callable]:
        """
        Get the list of callbacks to use.

        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        """
        return self._custom_callbacks if self._custom_callbacks else self._available_handlers

    def get_handler_names(self) -> List[str]:
        """
        Get the names of available handlers.

        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        """
        return list(self._handler_names)

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
        if callback not in self._custom_callbacks:
            self._custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        """Clear all custom callbacks."""
        self._custom_callbacks.clear()

    def __repr__(self) -> str:
        """String representation of the ObservabilityManager."""
        total = len(self.get_callbacks())
        return f"<{self.__class__.__name__} callbacks={total} ({'custom' if self._custom_callbacks else 'available'})>"

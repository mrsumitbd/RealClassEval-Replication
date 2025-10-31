
import importlib
import os
from typing import Callable, List, Optional, Dict


class ObservabilityManager:
    """
    Manages observability callbacks for MCP agents.
    This class provides a centralized way to collect and manage callbacks
    from various observability platforms (Langfuse, Laminar, etc.).
    """

    # Known handler names and the module path pattern that may contain the callback.
    _KNOWN_HANDLERS: Dict[str, str] = {
        "Langfuse": "observability.langfuse_handler",
        "Laminar": "observability.laminar_handler",
    }

    def __init__(self, custom_callbacks: Optional[List[Callable]] = None):
        """
        Initialize the ObservabilityManager.

        Args:
            custom_callbacks: Optional list of custom callbacks to use instead of defaults.
        """
        self._custom_callbacks: List[Callable] = list(
            custom_callbacks) if custom_callbacks else []
        self._available_handlers: Dict[str, Callable] = {}
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        """Collect all available observability handlers from configured platforms."""
        for name, module_path in self._KNOWN_HANDLERS.items():
            try:
                module = importlib.import_module(module_path)
                # Prefer a 'handler' attribute; fall back to the module itself if callable.
                callback = getattr(module, "handler", None)
                if callback is None and callable(module):
                    callback = module
                if callback and callable(callback):
                    self._available_handlers[name] = callback
            except Exception:
                # If the module cannot be imported or does not provide a callable,
                # silently ignore it – the platform is simply not available.
                continue

    def get_callbacks(self) -> List[Callable]:
        """
        Get the list of callbacks to use.

        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        """
        return self._custom_callbacks if self._custom_callbacks else list(self._available_handlers.values())

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
        if not callable(callback):
            raise TypeError("callback must be callable")
        self._custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        """Clear all custom callbacks."""
        self._custom_callbacks.clear()

    def __repr__(self) -> str:
        """String representation of the ObservabilityManager."""
        names = self.get_handler_names()
        custom = len(self._custom_callbacks)
        return (
            f"<ObservabilityManager "
            f"handlers={names} "
            f"custom_callbacks={custom}>"
        )

import importlib
from importlib.util import find_spec
from typing import Any


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
        self._handlers: dict[str, Any] = {}
        self._use_custom: bool = custom_callbacks is not None
        self._custom_callbacks: list = list(
            custom_callbacks) if custom_callbacks is not None else []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:
        '''Collect all available observability handlers from configured platforms.'''
        self._handlers.clear()

        def _try_import_handler(module_name: str, class_names: tuple[str, ...]) -> Any | None:
            try:
                mod = importlib.import_module(module_name)
            except Exception:
                return None
            for cls_name in class_names:
                cb_cls = getattr(mod, cls_name, None)
                if cb_cls is None:
                    continue
                try:
                    return cb_cls()
                except Exception:
                    continue
            return None

        # Langfuse
        if find_spec('langfuse') is not None:
            handler = None
            # Prefer explicit callback submodule if present
            if find_spec('langfuse.callback') is not None:
                handler = _try_import_handler(
                    'langfuse.callback', ('CallbackHandler', 'LangfuseCallbackHandler'))
            if handler is None:
                handler = _try_import_handler(
                    'langfuse', ('CallbackHandler', 'LangfuseCallbackHandler'))
            if handler is not None:
                self._handlers['Langfuse'] = handler

        # Laminar (best-effort, class names may vary across versions)
        if find_spec('laminar') is not None:
            handler = _try_import_handler(
                'laminar', ('CallbackHandler', 'LaminarCallbackHandler', 'Callback'))
            if handler is not None:
                self._handlers['Laminar'] = handler

    def get_callbacks(self) -> list:
        '''
        Get the list of callbacks to use.
        Returns:
            List of callbacks - either custom callbacks if provided,
            or all available observability handlers.
        '''
        if self._use_custom:
            return list(self._custom_callbacks)
        return list(self._handlers.values())

    def get_handler_names(self) -> list[str]:
        '''
        Get the names of available handlers.
        Returns:
            List of handler names (e.g., ["Langfuse", "Laminar"])
        '''
        return list(self._handlers.keys())

    def has_callbacks(self) -> bool:
        '''
        Check if any callbacks are available.
        Returns:
            True if callbacks are available, False otherwise.
        '''
        return len(self.get_callbacks()) > 0

    def add_callback(self, callback) -> None:
        '''
        Add a callback to the custom callbacks list.
        Args:
            callback: The callback to add.
        '''
        if not self._use_custom:
            self._use_custom = True
            self._custom_callbacks = []
        self._custom_callbacks.append(callback)

    def clear_callbacks(self) -> None:
        '''Clear all custom callbacks.'''
        self._use_custom = True
        self._custom_callbacks = []

    def __repr__(self) -> str:
        '''String representation of the ObservabilityManager.'''
        mode = 'custom' if self._use_custom else 'auto'
        names = self.get_handler_names() if not self._use_custom else [
            '<custom>']
        return f'ObservabilityManager(mode={mode}, handlers={names}, callbacks={len(self.get_callbacks())})'

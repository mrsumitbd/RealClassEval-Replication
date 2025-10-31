
import inspect
import pkgutil
import importlib
import logging


class ObservabilityManager:

    def __init__(self, custom_callbacks: list | None = None):

        self._callbacks = custom_callbacks if custom_callbacks is not None else []
        self._handler_names = []
        self._collect_available_handlers()

    def _collect_available_handlers(self) -> None:

        for finder, name, ispkg in pkgutil.iter_modules():
            if name.startswith('observability_'):
                module = importlib.import_module(name)
                for _, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and hasattr(obj, 'handle'):
                        self._handler_names.append(obj.__name__)

    def get_callbacks(self) -> list:

        return self._callbacks

    def get_handler_names(self) -> list[str]:

        return self._handler_names

    def has_callbacks(self) -> bool:

        return len(self._callbacks) > 0

    def add_callback(self, callback) -> None:

        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def clear_callbacks(self) -> None:

        self._callbacks.clear()

    def __repr__(self) -> str:

        return f"ObservabilityManager(callbacks={self._callbacks}, handler_names={self._handler_names})"

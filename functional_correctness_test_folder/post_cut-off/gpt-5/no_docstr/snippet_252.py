from typing import Callable, List, Tuple, Any, Optional
from threading import RLock


class BasePlugin:
    def __init__(self) -> None:
        self._frontend_entries: List[Tuple[str, str]] = []
        self._backend_registrars: List[Callable[[Any], None]] = []
        self._lock = RLock()

    def add_frontend(self, path: str, resource: str) -> None:
        if not isinstance(path, str) or not isinstance(resource, str):
            raise TypeError("path and resource must be strings")
        with self._lock:
            self._frontend_entries.append((path, resource))

    def add_backend_registrar(self, registrar: Callable[[Any], None]) -> None:
        if not callable(registrar):
            raise TypeError("registrar must be callable")
        with self._lock:
            self._backend_registrars.append(registrar)

    def clear_frontend(self) -> None:
        with self._lock:
            self._frontend_entries.clear()

    def clear_backend(self) -> None:
        with self._lock:
            self._backend_registrars.clear()

    def has_frontend(self) -> bool:
        with self._lock:
            return bool(self._frontend_entries)

    def has_backend(self) -> bool:
        with self._lock:
            return bool(self._backend_registrars)

    def register_frontend(self, register_func: Callable[[str, str], None]) -> None:
        if not callable(register_func):
            raise TypeError("register_func must be callable")
        with self._lock:
            for path, resource in list(self._frontend_entries):
                register_func(path, resource)

    def register_backend(self, app) -> None:
        with self._lock:
            for registrar in list(self._backend_registrars):
                registrar(app)


from typing import Callable, Any, Optional


class BasePlugin:
    """
    A minimal base class for plugins that can register frontend and backend
    components. Subclasses can override `register_frontend` and `register_backend`
    to perform custom registration logic.
    """

    def __init__(self) -> None:
        # Store the frontend registration callback and backend application
        self._frontend_register: Optional[Callable[[str, str], None]] = None
        self._backend_app: Optional[Any] = None

    def register_frontend(self, register_func: Callable[[str, str], None]) -> None:
        """
        Register a callback that will be used to expose frontend routes or
        components. The callback should accept a name and a path.
        """
        self._frontend_register = register_func

    def register_backend(self, app: Any) -> None:
        """
        Register a backend application instance (e.g., Flask, FastAPI, etc.).
        """
        self._backend_app = app

    # Convenience helpers -------------------------------------------------

    def add_frontend_route(self, name: str, path: str) -> None:
        """
        Register a frontend route using the stored callback.
        """
        if self._frontend_register is None:
            raise RuntimeError("Frontend register function not set")
        self._frontend_register(name, path)

    def add_backend_route(self, path: str, handler: Callable[..., Any]) -> None:
        """
        Register a backend route using the stored application instance.
        Supports Flask and FastAPI style apps.
        """
        if self._backend_app is None:
            raise RuntimeError("Backend app not set")

        # Flask style
        if hasattr(self._backend_app, "add_url_rule"):
            self._backend_app.add_url_rule(path, view_func=handler)
            return

        # FastAPI style
        if hasattr(self._backend_app, "get"):
            self._backend_app.get(path)(handler)
            return

        raise TypeError("Unsupported backend app type")

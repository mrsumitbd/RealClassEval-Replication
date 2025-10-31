
from typing import Callable


class BasePlugin:

    def register_frontend(self, register_func: Callable[[str, str], None]):
        register_func("frontend_key", "frontend_value")

    def register_backend(self, app):
        app.register("backend_key", "backend_value")

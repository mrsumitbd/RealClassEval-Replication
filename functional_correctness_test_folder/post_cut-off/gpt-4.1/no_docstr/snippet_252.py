
from typing import Callable


class BasePlugin:

    def register_frontend(self, register_func: Callable[[str, str], None]):
        """
        Register frontend assets or routes.
        Should be overridden by subclasses.
        """
        pass

    def register_backend(self, app):
        """
        Register backend routes or handlers.
        Should be overridden by subclasses.
        """
        pass

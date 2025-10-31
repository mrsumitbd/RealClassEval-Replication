
from typing import Callable
from flask import Flask


class BasePlugin:
    """
    Base class for plugins.
    """

    def register_frontend(self, register_func: Callable[[str, str], None]):
        """
        Registers frontend assets.

        Args:
        - register_func: A function that takes two string arguments, 
                         the first being the asset type and the second being the asset content.
        """
        pass

    def register_backend(self, app: Flask):
        """
        Registers backend routes and configurations.

        Args:
        - app: A Flask application instance.
        """
        pass

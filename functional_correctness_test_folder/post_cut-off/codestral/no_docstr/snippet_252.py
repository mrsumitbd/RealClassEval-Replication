
class BasePlugin:

    def register_frontend(self, register_func: Callable[[str, str], None]):

        pass

    def register_backend(self, app):

        pass

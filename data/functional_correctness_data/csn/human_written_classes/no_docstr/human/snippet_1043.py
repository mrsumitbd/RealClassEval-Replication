import os

class EnvironmentResolver:

    def get(self, item, default=None):
        return os.environ.get(item, default)

    def __str__(self):
        return f'environemnt'
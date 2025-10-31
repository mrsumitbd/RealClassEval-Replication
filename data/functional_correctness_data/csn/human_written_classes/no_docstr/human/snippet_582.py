from functools import wraps

class Command:
    _registry = dict()

    def __init__(self, aliases, permission, scope):
        self.aliases = aliases
        self.permission = permission
        self.scope = scope

    def __call__(self, _command):

        @wraps(_command)
        def wrapper(*args, **kwds):
            return _command(*args, **kwds)
        return wrapper
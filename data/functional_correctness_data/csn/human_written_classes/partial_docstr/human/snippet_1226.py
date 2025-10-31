import os

class Message:
    """A linter message to the user."""
    level = None

    def __init__(self, name, msg, *args, **kwargs):
        self.name = name
        self.location = kwargs.pop('location', None)
        self.api_name = kwargs.pop('api_name', None)
        self.msg = msg.format(*args, **kwargs)

    def __str__(self):
        output = '{}: API {} at {}: {}'.format(self.level.name.title(), self.api_name, self.name, self.msg)
        if self.location is None:
            return output
        else:
            return '{}:{}: {}'.format(os.path.relpath(self.location['filename']), self.location['lineno'], output)
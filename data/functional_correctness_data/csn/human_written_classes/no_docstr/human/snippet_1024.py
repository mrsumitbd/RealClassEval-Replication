import json

class StoryPartLeaf:

    def __init__(self, fn):
        self.fn = fn

    @property
    def __name__(self):
        return self.fn.__name__

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __repr__(self):
        return json.dumps({'type': 'StoryPartLeaf', 'name': self.__name__})
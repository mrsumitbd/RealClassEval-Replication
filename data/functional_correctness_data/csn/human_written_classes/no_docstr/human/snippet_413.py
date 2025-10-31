import json

class LazyJSON:

    def __init__(self, content):
        self.text = content
        self._json = None

    @property
    def json(self):
        if self._json is None:
            self._json = json.loads(self.text)
        return self._json

    def __getitem__(self, key):
        return self.json[key]
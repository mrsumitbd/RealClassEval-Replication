class _JSONPath:

    def __init__(self, path):
        self._path = path

    def __str__(self):
        return self._path

    def append(self, item):
        return _JSONPath('{0}[{1}]'.format(self._path, repr(item)))
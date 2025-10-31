import code
from types import CodeType

class _ConsoleLoader:

    def __init__(self):
        self._storage = {}

    def register(self, code, source):
        self._storage[id(code)] = source
        for var in code.co_consts:
            if isinstance(var, CodeType):
                self._storage[id(var)] = source

    def get_source_by_code(self, code):
        try:
            return self._storage[id(code)]
        except KeyError:
            pass
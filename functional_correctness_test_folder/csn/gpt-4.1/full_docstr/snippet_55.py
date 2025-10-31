
class Exporter:
    '''Manages exporting of symbols from the module.
    Grabs a reference to `globals()` for a module and provides a decorator to add
    functions and classes to `__all__` rather than requiring a separately maintained list.
    Also provides a context manager to do this for instances by adding all instances added
    within a block to `__all__`.
    '''

    def __init__(self, globls):
        '''Initialize the Exporter.'''
        self._globals = globls
        if '__all__' not in self._globals:
            self._globals['__all__'] = []
        self._all = self._globals['__all__']
        self._in_context = False
        self._before = None

    def export(self, defn):
        '''Declare a function or class as exported.'''
        name = defn.__name__
        if name not in self._all:
            self._all.append(name)
        return defn

    def __enter__(self):
        '''Start a block tracking all instances created at global scope.'''
        self._in_context = True
        self._before = set(self._globals.keys())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the instance tracking block.'''
        after = set(self._globals.keys())
        new_names = after - self._before
        for name in new_names:
            if name not in self._all and not name.startswith('_'):
                self._all.append(name)
        self._in_context = False
        self._before = None

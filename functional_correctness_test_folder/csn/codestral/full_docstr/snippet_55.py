
class Exporter:
    '''Manages exporting of symbols from the module.
    Grabs a reference to `globals()` for a module and provides a decorator to add
    functions and classes to `__all__` rather than requiring a separately maintained list.
    Also provides a context manager to do this for instances by adding all instances added
    within a block to `__all__`.
    '''

    def __init__(self, globls):
        '''Initialize the Exporter.'''
        self.globls = globls
        self._all = globls.get('__all__', [])
        self._tracking = False
        self._tracked = []

    def export(self, defn):
        '''Declare a function or class as exported.'''
        if defn.__name__ not in self._all:
            self._all.append(defn.__name__)
        if self._tracking:
            self._tracked.append(defn.__name__)
        return defn

    def __enter__(self):
        '''Start a block tracking all instances created at global scope.'''
        self._tracking = True
        self._tracked = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the instance tracking block.'''
        self._tracking = False
        for name in self._tracked:
            if name not in self._all:
                self._all.append(name)
        self.globls['__all__'] = self._all


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
        if '__all__' not in globls:
            globls['__all__'] = []
        self._exported_instances = []

    def export(self, defn):
        '''Declare a function or class as exported.'''
        self.globls['__all__'].append(defn.__name__)
        return defn

    def __enter__(self):
        '''Start a block tracking all instances created at global scope.'''
        self._original_globals = set(self.globls.keys())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the instance tracking block.'''
        new_keys = set(self.globls.keys()) - self._original_globals
        for key in new_keys:
            if not key.startswith('_'):
                self.globls['__all__'].append(key)
        self._original_globals = None

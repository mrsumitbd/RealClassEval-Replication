
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
        self.globls.setdefault('__all__', [])

    def export(self, defn):
        '''Declare a function or class as exported.'''
        if defn.__name__ not in self.globls['__all__']:
            self.globls['__all__'].append(defn.__name__)
        return defn

    def __enter__(self):
        '''Start a block tracking all instances created at global scope.'''
        self._original_all = self.globls['__all__'][:]
        self._created = set()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the instance tracking block.'''
        new_symbols = [
            name for name in self.globls if name not in self._original_all and not name.startswith('_')]
        self.globls['__all__'].extend(new_symbols)
        self.globls['__all__'] = list(
            set(self.globls['__all__']))  # Ensure uniqueness

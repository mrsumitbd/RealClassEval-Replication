
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
        if '__all__' not in self.globls:
            self.globls['__all__'] = []

    def export(self, defn):
        '''Declare a function or class as exported.'''
        self.globls['__all__'].append(defn.__name__)
        return defn

    def __enter__(self):
        '''Start a block tracking all instances created at global scope.'''
        self.instances = set(self.globls.keys())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the instance tracking block.'''
        new_instances = set(self.globls.keys()) - self.instances
        self.globls['__all__'].extend(new_instances)

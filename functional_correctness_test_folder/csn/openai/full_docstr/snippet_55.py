
import types


class Exporter:
    '''Manages exporting of symbols from the module.
    Grabs a reference to `globals()` for a module and provides a decorator to add
    functions and classes to `__all__` rather than requiring a separately maintained list.
    Also provides a context manager to do this for instances by adding all instances added
    within a block to `__all__`.
    '''

    def __init__(self, globls):
        '''Initialize the Exporter.'''
        self.globals = globls
        # Ensure __all__ exists and is a list
        if '__all__' not in self.globals or not isinstance(self.globals['__all__'], list):
            self.globals['__all__'] = []
        self._all = self.globals['__all__']
        self._prev_keys = None

    def export(self, defn):
        '''Declare a function or class as exported.'''
        name = getattr(defn, '__name__', None)
        if name and name not in self._all:
            self._all.append(name)
        return defn

    def __enter__(self):
        '''Start a block tracking all instances created at global scope.'''
        self._prev_keys = set(self.globals.keys())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the instance tracking block.'''
        # Determine new global names added inside the block
        new_keys = set(self.globals.keys()) - self._prev_keys
        for key in new_keys:
            val = self.globals[key]
            # Skip functions and classes
            if isinstance(val, (types.FunctionType, type)):
                continue
            # Check if the value's type is a class defined in this module
            cls = type(val)
            if cls in self.globals.values() and isinstance(cls, type):
                if key not in self._all:
                    self._all.append(key)
        # Do not suppress exceptions
        return False

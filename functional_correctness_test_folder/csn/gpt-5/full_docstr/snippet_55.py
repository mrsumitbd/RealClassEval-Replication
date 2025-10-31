class Exporter:
    '''Manages exporting of symbols from the module.
    Grabs a reference to `globals()` for a module and provides a decorator to add
    functions and classes to `__all__` rather than requiring a separately maintained list.
    Also provides a context manager to do this for instances by adding all instances added
    within a block to `__all__`.
    '''

    def __init__(self, globls):
        '''Initialize the Exporter.'''
        if not isinstance(globls, dict):
            raise TypeError("globls must be a globals() dict")
        self._globals = globls
        if "__all__" not in self._globals or not isinstance(self._globals["__all__"], list):
            self._globals["__all__"] = []
        self._stack = []

    def _append_to_all(self, name):
        all_list = self._globals["__all__"]
        if name not in all_list and not name.startswith("_"):
            all_list.append(name)

    def export(self, defn):
        '''Declare a function or class as exported.'''
        name = getattr(defn, "__name__", None)
        if not name:
            raise ValueError(
                "export can only be used on named functions/classes")
        self._append_to_all(name)
        return defn

    def __enter__(self):
        '''Start a block tracking all instances created at global scope.'''
        self._stack.append(set(self._globals.keys()))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the instance tracking block.'''
        if not self._stack:
            return False
        before = self._stack.pop()
        after = set(self._globals.keys())
        added = after - before
        for name in added:
            self._append_to_all(name)
        return False

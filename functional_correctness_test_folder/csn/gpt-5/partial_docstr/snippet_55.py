class Exporter:
    def __init__(self, globls):
        if not isinstance(globls, dict):
            raise TypeError("globls must be a dict of globals()")
        self._g = globls
        self._pre_keys = None
        self._ensure_all()

    def _ensure_all(self):
        allv = self._g.get('__all__')
        if allv is None:
            self._g['__all__'] = []
        elif not isinstance(allv, list):
            # Coerce to list for consistent behavior
            self._g['__all__'] = list(allv)

    def _add_to_all(self, name):
        if not name or not isinstance(name, str):
            return
        if name == '__all__' or name.startswith('_'):
            return
        allv = self._g['__all__']
        if name not in allv:
            allv.append(name)

    def export(self, defn):
        import types

        def _export_one(item):
            # If string, just export by name (must already exist in globals)
            if isinstance(item, str):
                if item in self._g:
                    self._add_to_all(item)
                else:
                    # Still add to __all__ to allow forward declaration style
                    self._add_to_all(item)
                return item

            # If it looks like a definition (function/class/object with __name__)
            name = getattr(item, '__name__', None)
            if not name:
                raise ValueError("Cannot export object without a __name__")
            # Place into globals if not already there
            if self._g.get(name) is not item:
                self._g[name] = item
            # Ensure module name matches current module if applicable
            if hasattr(item, '__module__'):
                try:
                    modname = self._g.get('__name__')
                    if isinstance(modname, str):
                        item.__module__ = modname
                except Exception:
                    pass
            self._add_to_all(name)
            return item

        if isinstance(defn, (list, tuple, set)):
            return [self.export(x) for x in defn]
        return _export_one(defn)

    def __enter__(self):
        '''Start a block tracking all instances created at global scope.'''
        self._ensure_all()
        self._pre_keys = set(self._g.keys())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the instance tracking block.'''
        if exc_type is not None:
            # Do not modify exports if the block failed
            self._pre_keys = None
            return False

        import types

        if self._pre_keys is None:
            return False

        new_keys = set(self._g.keys()) - self._pre_keys
        for name in sorted(new_keys):
            if name == '__all__' or name.startswith('_'):
                continue
            val = self._g.get(name)
            if isinstance(val, types.ModuleType):
                continue
            self._add_to_all(name)

        self._pre_keys = None
        return False

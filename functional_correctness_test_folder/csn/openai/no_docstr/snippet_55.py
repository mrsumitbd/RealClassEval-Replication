
class Exporter:
    def __init__(self, globls):
        """
        Create an Exporter that will temporarily add definitions to the given
        globals dictionary.  The exporter keeps track of original values so
        they can be restored when the context manager exits.
        """
        self.globals = globls
        self._original = {}   # name -> original value
        self._added = set()   # names that were added during export

    def _export(self, name, obj):
        if name in self.globals:
            # Preserve the original value
            if name not in self._original:
                self._original[name] = self.globals[name]
        else:
            # Mark as newly added
            self._added.add(name)
        self.globals[name] = obj

    def export(self, defn):
        """
        Export a definition or a collection of definitions to the globals.
        * If `defn` is a dict, each key/value pair is exported.
        * If `defn` is an iterable of objects, each object's __name__ is used.
        * Otherwise, `defn` is assumed to be a single object and its __name__
          is exported.
        """
        if isinstance(defn, dict):
            for name, obj in defn.items():
                self._export(name, obj)
        elif isinstance(defn, (list, tuple, set)):
            for obj in defn:
                if hasattr(obj, "__name__"):
                    self._export(obj.__name__, obj)
                else:
                    raise TypeError(
                        f"Object {obj!r} has no __name__ attribute")
        else:
            if hasattr(defn, "__name__"):
                self._export(defn.__name__, defn)
            else:
                raise TypeError(f"Object {defn!r} has no __name__ attribute")

    def __enter__(self):
        """
        Enter the context manager.  Nothing special is needed here; we simply
        return the exporter instance so that the caller can use its methods.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager.  Restore any original values that were
        overwritten and delete any names that were added during export.
        """
        # Restore original values
        for name, original in self._original.items():
            self.globals[name] = original

        # Remove newly added names
        for name in self._added:
            self.globals.pop(name, None)

        # Clear tracking structures for potential reuse
        self._original.clear()
        self._added.clear()

        # Returning False propagates any exception that occurred
        return False

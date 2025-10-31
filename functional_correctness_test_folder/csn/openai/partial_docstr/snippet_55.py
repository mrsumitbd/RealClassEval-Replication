
class Exporter:
    """
    A context manager that tracks definitions created inside a block and
    injects them into a supplied globals dictionary when the block exits.
    """

    def __init__(self, globls):
        """
        Parameters
        ----------
        globls : dict
            The globals dictionary where exported names will be inserted.
        """
        self.globls = globls
        self._exports = []

    def export(self, defn):
        """
        Register a definition (function, class, or any object with a __name__
        attribute) to be exported when the context exits.

        Parameters
        ----------
        defn : object
            The object to export.
        """
        if not hasattr(defn, "__name__"):
            raise TypeError("exported objects must have a __name__ attribute")
        self._exports.append(defn)

    def __enter__(self):
        """
        Start a block tracking all definitions created at global scope.
        """
        # Nothing special to do on enter; just return self for chaining.
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the instance tracking block and inject all registered
        definitions into the supplied globals dictionary.
        """
        for obj in self._exports:
            self.globls[obj.__name__] = obj
        # Clear the list to avoid leaking references.
        self._exports.clear()
        # Returning False propagates any exception that occurred.
        return False

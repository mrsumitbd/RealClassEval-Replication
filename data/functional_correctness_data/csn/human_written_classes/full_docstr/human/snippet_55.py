class Exporter:
    """Manages exporting of symbols from the module.

    Grabs a reference to `globals()` for a module and provides a decorator to add
    functions and classes to `__all__` rather than requiring a separately maintained list.
    Also provides a context manager to do this for instances by adding all instances added
    within a block to `__all__`.
    """

    def __init__(self, globls):
        """Initialize the Exporter."""
        self.globls = globls
        self.exports = globls.setdefault('__all__', [])

    def export(self, defn):
        """Declare a function or class as exported."""
        self.exports.append(defn.__name__)
        return defn

    def __enter__(self):
        """Start a block tracking all instances created at global scope."""
        self.start_vars = set(self.globls)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the instance tracking block."""
        self.exports.extend(set(self.globls) - self.start_vars)
        del self.start_vars
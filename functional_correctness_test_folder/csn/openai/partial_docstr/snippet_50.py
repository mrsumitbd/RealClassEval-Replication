class MetPyChecker:
    name = "metpy-checker"
    version = "0.1.0"

    def __init__(self, tree):
        """Initialize the plugin."""
        self.tree = tree

    def run(self):
        """Run the checker and return a list of errors."""
        # No checks implemented; return an empty list.
        return []

    def error(self, err):
        """Format an error tuple."""
        # err is expected to be a tuple (line, col, message)
        line, col, msg = err
        return (line, col, msg, type(self))

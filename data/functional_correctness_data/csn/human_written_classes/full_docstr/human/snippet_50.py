class MetPyChecker:
    """Flake8 plugin class to check MetPy style/best practice."""
    name = __name__
    version = '1.0'

    def __init__(self, tree):
        """Initialize the plugin."""
        self.tree = tree

    def run(self):
        """Run the plugin and yield errors."""
        visitor = MetPyVisitor()
        visitor.visit(self.tree)
        for err in visitor.errors:
            yield self.error(err)

    def error(self, err):
        """Format errors into Flake8's required format."""
        return (err.lineno, err.col, f'MPY{err.code:03d}: Multiplying/dividing by units--use units.Quantity()', type(self))
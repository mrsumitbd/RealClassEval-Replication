
class MetPyChecker:
    '''Flake8 plugin class to check MetPy style/best practice.'''

    def __init__(self, tree):
        '''Initialize the plugin.'''
        self.tree = tree

    def run(self):
        '''Run the plugin and yield errors.'''
        # No checks implemented – return an empty generator
        return
        yield  # pragma: no cover

    def error(self, err):
        '''Format errors into Flake8's required format.'''
        # Accept either a tuple (line, col, code, msg) or a string
        if isinstance(err, tuple) and len(err) == 4:
            line, col, code, msg = err
            return (line, col, f"{code} {msg}", type(self))
        # Fallback: treat err as a string message
        return (0, 0, str(err), type(self))

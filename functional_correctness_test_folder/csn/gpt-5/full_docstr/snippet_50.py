class MetPyChecker:
    '''Flake8 plugin class to check MetPy style/best practice.'''

    name = 'metpy-checker'
    version = '0.1.0'

    def __init__(self, tree, filename=None):
        '''Initialize the plugin.'''
        self.tree = tree
        self.filename = filename or ''
        self._errors = []

    def run(self):
        '''Run the plugin and yield errors.'''
        for err in self._errors:
            yield self.error(err)

    def error(self, err):
        '''Format errors into Flake8's required format.'''
        if isinstance(err, dict):
            line = int(err.get('line', 1) or 1)
            col = int(err.get('col', 0) or 0)
            msg = err.get('msg', 'MPY000 MetPy checker error')
        else:
            try:
                line, col, msg = err[:3]
            except Exception:
                line, col, msg = 1, 0, 'MPY000 MetPy checker error'
        return (line, col, msg, type(self))

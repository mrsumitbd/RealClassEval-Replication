
class MetPyChecker:
    '''Flake8 plugin class to check MetPy style/best practice.'''

    def __init__(self, tree):
        '''Initialize the plugin.'''
        self.tree = tree

    def run(self):
        '''Run the plugin and yield errors.'''
        yield from []

    def error(self, err):
        '''Format errors into Flake8's required format.'''
        return (
            err.get('line', 0),
            err.get('col', 0),
            err.get('message', ''),
            type(self)
        )

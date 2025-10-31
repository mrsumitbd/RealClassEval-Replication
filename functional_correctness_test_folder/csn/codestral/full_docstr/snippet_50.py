
class MetPyChecker:
    '''Flake8 plugin class to check MetPy style/best practice.'''

    def __init__(self, tree):
        '''Initialize the plugin.'''
        self.tree = tree

    def run(self):
        '''Run the plugin and yield errors.'''
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'metpy':
                        yield self.error(node.lineno, node.col_offset, "MPY001 MetPy import found")

    def error(self, line, col, message):
        '''Format errors into Flake8's required format.'''
        return line, col, message, type(self)

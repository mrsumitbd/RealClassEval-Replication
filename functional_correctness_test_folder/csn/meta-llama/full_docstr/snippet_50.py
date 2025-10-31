
import ast


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
                    if alias.name == 'matplotlib.pyplot':
                        yield self.error('MPT001', node.lineno, node.col_offset,
                                         'Import matplotlib.pyplot directly')
            elif isinstance(node, ast.ImportFrom):
                if node.module == 'matplotlib.pyplot':
                    yield self.error('MPT002', node.lineno, node.col_offset,
                                     'Import from matplotlib.pyplot directly')

    def error(self, code, lineno, col_offset, msg):
        '''Format errors into Flake8's required format.'''
        text = f'{code} {msg}'
        return lineno, col_offset, text, type(self)

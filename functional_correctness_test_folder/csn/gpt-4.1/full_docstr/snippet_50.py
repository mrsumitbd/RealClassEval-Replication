
class MetPyChecker:
    '''Flake8 plugin class to check MetPy style/best practice.'''

    name = "metpy-checker"
    version = "0.1.0"

    def __init__(self, tree):
        '''Initialize the plugin.'''
        self.tree = tree

    def run(self):
        '''Run the plugin and yield errors.'''
        for node in ast.walk(self.tree):
            # Example check: discourage use of 'import *'
            if isinstance(node, ast.ImportFrom):
                if node.names and any(alias.name == '*' for alias in node.names):
                    yield self.error((
                        node.lineno,
                        node.col_offset,
                        "MPY001: Do not use 'import *' (MetPy best practice)",
                        type(self)
                    ))
            # Example check: discourage use of 'eval'
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and node.func.id == 'eval':
                    yield self.error((
                        node.lineno,
                        node.col_offset,
                        "MPY002: Do not use 'eval' (MetPy best practice)",
                        type(self)
                    ))

    def error(self, err):
        '''Format errors into Flake8's required format.'''
        return err

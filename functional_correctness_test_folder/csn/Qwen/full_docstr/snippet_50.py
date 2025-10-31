
class MetPyChecker:
    '''Flake8 plugin class to check MetPy style/best practice.'''

    def __init__(self, tree):
        '''Initialize the plugin.'''
        self.tree = tree

    def run(self):
        '''Run the plugin and yield errors.'''
        for node in self.tree.body:
            if isinstance(node, ast.FunctionDef) and not node.docstring:
                yield (node.lineno, node.col_offset, 'M001 Function missing docstring', type(self))
            # Additional checks can be added here

    def error(self, err):
        '''Format errors into Flake8's required format.'''
        return f"{err.lineno}:{err.col_offset}: {err.msg}"

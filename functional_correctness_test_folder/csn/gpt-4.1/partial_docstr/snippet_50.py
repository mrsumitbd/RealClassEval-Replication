
class MetPyChecker:

    def __init__(self, tree):
        '''Initialize the plugin.'''
        self.tree = tree

    def run(self):
        """
        Generator that yields errors found in the AST.
        For demonstration, let's check for 'import metpy' statements.
        """
        import ast
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'metpy':
                        yield (
                            node.lineno,
                            node.col_offset,
                            "MPY001 Do not import metpy directly.",
                            type(self)
                        )
            elif isinstance(node, ast.ImportFrom):
                if node.module == 'metpy':
                    yield (
                        node.lineno,
                        node.col_offset,
                        "MPY001 Do not import from metpy directly.",
                        type(self)
                    )

    def error(self, err):
        """
        Format the error tuple as a string.
        """
        lineno, col, msg, _ = err
        return f"{lineno}:{col}: {msg}"

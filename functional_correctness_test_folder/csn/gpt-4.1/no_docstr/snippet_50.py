
class MetPyChecker:

    def __init__(self, tree):
        self.tree = tree
        self.errors = []

    def run(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'metpy':
                        yield (node.lineno, node.col_offset, "MPY001 Do not import metpy directly", type(self))
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith('metpy'):
                    yield (node.lineno, node.col_offset, "MPY001 Do not import metpy directly", type(self))
        for err in self.errors:
            yield err

    def error(self, err):
        self.errors.append(err)

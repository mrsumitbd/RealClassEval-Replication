
class MetPyChecker:

    def __init__(self, tree):
        self.tree = tree
        self.errors = []

    def run(self):
        for node in self.tree.walk():
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr.startswith('metpy'):
                        self.check_metpy_call(node)

    def error(self, err):
        self.errors.append(err)

    def check_metpy_call(self, node):
        # Example check: Ensure metpy functions are called with at least one argument
        if len(node.args) < 1:
            self.error(
                f"MetPy function called without arguments at line {node.lineno}")

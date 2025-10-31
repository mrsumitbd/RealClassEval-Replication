
class MetPyChecker:

    def __init__(self, tree):

        self.tree = tree
        self.errors = []

    def run(self):

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if not node.args.args:
                    self.error(f"Function '{node.name}' has no arguments")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'metpy':
                        self.error(
                            "Importing 'metpy' directly is not allowed. Use 'import metpy.calc as mpcalc' instead")
            elif isinstance(node, ast.ImportFrom):
                if node.module == 'metpy':
                    self.error(
                        "Importing from 'metpy' directly is not allowed. Use 'import metpy.calc as mpcalc' instead")

    def error(self, err):

        self.errors.append(err)

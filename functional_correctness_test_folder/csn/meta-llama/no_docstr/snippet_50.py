
import ast


class MetPyChecker:

    def __init__(self, tree):
        self.tree = tree
        self.errors = []

    def run(self):
        # Assuming tree is an Abstract Syntax Tree (AST) of Python code
        # and we're checking for some MetPy specific rules or best practices
        # For demonstration, let's check for usage of certain functions
        for node in self.tree.body:
            if isinstance(node, ast.FunctionDef):
                for sub_node in ast.walk(node):
                    if isinstance(sub_node, ast.Call):
                        if isinstance(sub_node.func, ast.Name) and sub_node.func.id == 'some_metpy_function':
                            # Example check: Ensure 'some_metpy_function' is used correctly
                            if len(sub_node.args) != 2:
                                self.error(
                                    f"Incorrect number of arguments to 'some_metpy_function' at line {sub_node.lineno}")

    def error(self, err):
        self.errors.append(err)


def main():
    # Example usage
    code = """
def my_function():
    some_metpy_function(1)  # This should trigger an error
    some_metpy_function(1, 2)  # This should not trigger an error
"""
    tree = ast.parse(code)
    checker = MetPyChecker(tree)
    checker.run()
    for error in checker.errors:
        print(error)


if __name__ == "__main__":
    main()

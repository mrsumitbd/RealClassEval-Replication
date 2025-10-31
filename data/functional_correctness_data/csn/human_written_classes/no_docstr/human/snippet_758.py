class Plugin:
    name = 'globus-cli-flake8'
    version = '0.0.1'

    def __init__(self, tree) -> None:
        self.tree = tree

    def run(self):
        visitor = CLIVisitor()
        visitor.visit(self.tree)
        for lineno, col, code in visitor.collect:
            yield (lineno, col, CODEMAP[code], type(self))
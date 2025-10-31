class MetPyChecker:
    name = "metpy-checker"
    version = "0.1.0"

    CODE_WILDCARD_IMPORT = "MPY100"
    MSG_WILDCARD_IMPORT = "MPY100 Avoid 'import *' from MetPy; import explicit names."

    def __init__(self, tree):
        '''Initialize the plugin.'''
        self.tree = tree
        self._errors = []

    def run(self):
        if self.tree is None:
            return
        import ast

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                if mod.startswith("metpy"):
                    for alias in node.names:
                        if alias.name == "*":
                            yield self.error(
                                {
                                    "line": getattr(node, "lineno", 1),
                                    "col": getattr(node, "col_offset", 0),
                                    "msg": self.MSG_WILDCARD_IMPORT,
                                }
                            )

    def error(self, err):
        return (err.get("line", 1), err.get("col", 0), err.get("msg", ""), type(self))

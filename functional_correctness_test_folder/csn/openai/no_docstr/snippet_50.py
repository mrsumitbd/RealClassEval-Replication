class MetPyChecker:
    def __init__(self, tree):
        self.tree = tree
        self.errors = []

    def run(self):
        # Placeholder for actual checking logic.
        # In a real implementation, this method would traverse `self.tree`
        # and call `self.error(...)` whenever a problem is found.
        return self.errors

    def error(self, err):
        self.errors.append(err)

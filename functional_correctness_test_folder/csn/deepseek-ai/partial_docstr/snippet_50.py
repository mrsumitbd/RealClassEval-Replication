
class MetPyChecker:

    def __init__(self, tree):
        '''Initialize the plugin.'''
        self.tree = tree
        self.errors = []

    def run(self):
        return self.errors

    def error(self, err):
        self.errors.append(err)

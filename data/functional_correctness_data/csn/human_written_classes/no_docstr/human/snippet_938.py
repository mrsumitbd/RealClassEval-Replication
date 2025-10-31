class DynamicLink:

    def __init__(self, source, target, node):
        self.source = source
        self.target = target
        self.node = node

    def __iter__(self):
        return iter((self.source, self.target, self.node))
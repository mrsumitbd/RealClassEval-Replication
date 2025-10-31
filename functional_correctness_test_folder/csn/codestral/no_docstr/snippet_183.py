
class Reader:

    def __init__(self, options):
        self.options = options

    def mangle(self, name, x):
        if name in self.options:
            return self.options[name](x)
        return x

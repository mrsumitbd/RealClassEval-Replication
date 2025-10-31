
class Reader:

    def __init__(self, options):
        self.options = options

    def mangle(self, name, x):
        return f"{name}_{x}"

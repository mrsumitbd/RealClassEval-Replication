
class Reader:

    def __init__(self, options):
        self.options = options

    def mangle(self, name, x):
        if 'prefix' in self.options:
            name = f"{self.options['prefix']}_{name}"
        if 'suffix' in self.options:
            name = f"{name}_{self.options['suffix']}"
        return f"{name}_{x}"

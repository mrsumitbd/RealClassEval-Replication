
class Reader:

    def __init__(self, options):
        self.options = options

    def mangle(self, name, x):
        if self.options.get('uppercase', False):
            name = name.upper()
        if self.options.get('reverse', False):
            name = name[::-1]
        if self.options.get('append', None) is not None:
            name = f"{name}{self.options['append']}"
        if self.options.get('prepend', None) is not None:
            name = f"{self.options['prepend']}{name}"
        if self.options.get('repeat', 1) > 1:
            name = name * self.options['repeat']
        if self.options.get('add_x', False):
            name = f"{name}{x}"
        return name

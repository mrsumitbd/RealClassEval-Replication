class KeyDefinition:

    def __init__(self, key, ext=None, default=None, convert=None):
        self.key = key
        self.ext = 0 if ext is None else ext
        self.default = default
        self.convert = convert

    def __call__(self, hdulist):
        value = hdulist[self.ext].header.get(self.key, self.default)
        if self.convert:
            return self.convert(value)
        return value
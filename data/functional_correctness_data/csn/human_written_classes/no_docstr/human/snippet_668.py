from shoebot.core.backend import cairo, gi, driver

class BackingStore:
    instance = None

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pycairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    @property
    def dimensions(self):
        return (self.width, self.height)

    @classmethod
    def get_backingstore(cls, width, height):
        if cls.instance is None or (width, height) != cls.instance.dimensions:
            cls.instance = BackingStore(width, height)
        return cls.instance
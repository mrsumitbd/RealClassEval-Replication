class OBJVector2:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def read(self, buf):
        self.x = buf.read_float()
        self.y = buf.read_float()
        return self

    def __str__(self):
        return '%s %s' % (self.x, 1 - self.y)
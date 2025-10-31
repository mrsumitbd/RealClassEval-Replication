class MagneticGrid:

    def __init__(self, padding=10):
        self.padding = padding
        self.stroke = _ctx.color(0.8)
        self.strokewidth = 0.5

    def draw(self):
        _ctx.nofill()
        _ctx.stroke(self.stroke)
        _ctx.strokewidth(self.strokewidth)
        _ctx.autoclosepath(False)
        _ctx.beginpath(0, 0)
        for x in range(_ctx.WIDTH):
            _ctx.moveto(x * self.padding, 0)
            _ctx.lineto(x * self.padding, _ctx.HEIGHT)
        for y in range(_ctx.HEIGHT / self.padding):
            _ctx.moveto(0, y * self.padding)
            _ctx.lineto(_ctx.WIDTH, y * self.padding)
        _ctx.endpath()

    def snap(self, x, y, treshold=0.4):
        l = x - x % self.padding
        t = y - y % self.padding
        r = l + self.padding
        b = t + self.padding
        treshold *= self.padding
        gx, gy = (x, y)
        if x - l < treshold and y - t < treshold:
            gx, gy = (l, t)
        if r - x < treshold and y - t < treshold:
            gx, gy = (r, t)
        if r - x < treshold and b - y < treshold:
            gx, gy = (r, b)
        if x - l < treshold and b - y < treshold:
            gx, gy = (l, b)
        return (gx, gy)
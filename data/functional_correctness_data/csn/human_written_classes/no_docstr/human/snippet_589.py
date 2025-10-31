from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red

class Entity:

    def __init__(self, display, x, y, speed=1):
        self.display = display
        self.x, self.y = (x, y)
        self.speed = speed

    def towards(self, entity):
        dx = entity.x - self.x
        dy = entity.y - self.y
        return vscale(self.speed, (sign(dx), sign(dy)))

    def die(self):
        self.speed = 0
        self.display = on_red(bold(yellow('o')))
import esper

class MovementProcessor:

    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, dt):
        for ent, (vel, rend) in esper.get_components(Velocity, Renderable):
            new_x = max(self.minx, rend.sprite.x + vel.x)
            new_y = max(self.miny, rend.sprite.y + vel.y)
            new_x = min(self.maxx - rend.w, new_x)
            new_y = min(self.maxy - rend.h, new_y)
            rend.sprite.position = (new_x, new_y, rend.sprite.z)
class Cycle:

    def __init__(self, attr_dict):
        self.appearance = attr_dict['appearance']
        self.x, self.y = (attr_dict['x'], attr_dict['y'])
        self.keylist = attr_dict['keys']
        self.dir = 0

    def move(self, grid):
        d = self.dir
        if d == 0:
            self.x += 1
        elif d == 90:
            self.y -= 1
        elif d == 180:
            self.x -= 1
        elif d == 270:
            self.y += 1

    def face(self, newdir):
        """ turn to face the given direction """
        if not newdir % 180 == self.dir % 180:
            self.dir = newdir

    def paint(self, grid):
        """ given a grid object, adds self to the grid and returns new grid
        """
        grid[self.y, self.x] = self.appearance
        return grid
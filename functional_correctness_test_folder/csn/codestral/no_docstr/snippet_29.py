
class RectangleBin:

    def __init__(self, bounds):
        self.bounds = bounds
        self.rectangles = []

    @property
    def extents(self):
        return self.bounds

    def insert(self, size, rotate=True):
        for rect in self.rectangles:
            if self._can_fit(rect, size, rotate):
                return True
        if self._can_fit((0, 0), size, rotate):
            self.rectangles.append((0, 0, size[0], size[1]))
            return True
        return False

    def _can_fit(self, rect, size, rotate):
        x, y, w, h = rect
        width, height = size
        if rotate:
            width, height = height, width
        if x + width <= self.bounds[0] and y + height <= self.bounds[1]:
            for other in self.rectangles:
                if not (x + width <= other[0] or x >= other[0] + other[2] or y + height <= other[1] or y >= other[1] + other[3]):
                    return False
            return True
        return False

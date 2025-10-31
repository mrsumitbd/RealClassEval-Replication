
class RectangleBin:

    def __init__(self, bounds):
        self.bounds = bounds
        self.items = []

    @property
    def extents(self):
        return self.bounds

    def insert(self, size, rotate=True):
        width, height = size
        if rotate:
            width, height = min(width, height), max(width, height)

        for item in self.items:
            if item['x'] + item['width'] <= self.bounds[0] and item['y'] + item['height'] <= self.bounds[1]:
                if item['x'] + width <= self.bounds[0] and item['y'] + height <= self.bounds[1]:
                    self.items.append(
                        {'x': item['x'] + item['width'], 'y': item['y'], 'width': width, 'height': height})
                    return True
                elif item['x'] + height <= self.bounds[0] and item['y'] + width <= self.bounds[1]:
                    self.items.append(
                        {'x': item['x'] + item['height'], 'y': item['y'], 'width': height, 'height': width})
                    return True
        if 0 + width <= self.bounds[0] and 0 + height <= self.bounds[1]:
            self.items.append(
                {'x': 0, 'y': 0, 'width': width, 'height': height})
            return True
        return False

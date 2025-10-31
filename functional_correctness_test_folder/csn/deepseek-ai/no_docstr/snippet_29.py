
class RectangleBin:

    def __init__(self, bounds):
        self.bounds = bounds
        self.used_rectangles = []
        self.free_rectangles = [
            {'x': 0, 'y': 0, 'width': bounds[0], 'height': bounds[1]}]

    @property
    def extents(self):
        max_width = 0
        max_height = 0
        for rect in self.used_rectangles:
            max_width = max(max_width, rect['x'] + rect['width'])
            max_height = max(max_height, rect['y'] + rect['height'])
        return (max_width, max_height)

    def insert(self, size, rotate=True):
        best_score = float('inf')
        best_rect = None
        best_fit = None

        width, height = size
        if rotate:
            rotated_width, rotated_height = height, width
        else:
            rotated_width, rotated_height = width, height

        for i, free_rect in enumerate(self.free_rectangles):
            if free_rect['width'] >= width and free_rect['height'] >= height:
                score = self._score_rect(width, height, free_rect)
                if score < best_score:
                    best_score = score
                    best_rect = {
                        'x': free_rect['x'], 'y': free_rect['y'], 'width': width, 'height': height}
                    best_fit = i
            if rotate and free_rect['width'] >= rotated_width and free_rect['height'] >= rotated_height:
                score = self._score_rect(
                    rotated_width, rotated_height, free_rect)
                if score < best_score:
                    best_score = score
                    best_rect = {'x': free_rect['x'], 'y': free_rect['y'],
                                 'width': rotated_width, 'height': rotated_height}
                    best_fit = i

        if best_rect is None:
            return None

        self._split_free_rect(best_fit, best_rect)
        self.used_rectangles.append(best_rect)
        return best_rect

    def _score_rect(self, width, height, free_rect):
        return free_rect['width'] - width + free_rect['height'] - height

    def _split_free_rect(self, index, rect):
        free_rect = self.free_rectangles.pop(index)

        # Split the remaining space into two rectangles (horizontal and vertical)
        if rect['x'] + rect['width'] < free_rect['x'] + free_rect['width']:
            new_width = (free_rect['x'] + free_rect['width']
                         ) - (rect['x'] + rect['width'])
            new_rect = {
                'x': rect['x'] + rect['width'],
                'y': free_rect['y'],
                'width': new_width,
                'height': free_rect['height']
            }
            self.free_rectangles.append(new_rect)

        if rect['y'] + rect['height'] < free_rect['y'] + free_rect['height']:
            new_height = (free_rect['y'] + free_rect['height']
                          ) - (rect['y'] + rect['height'])
            new_rect = {
                'x': free_rect['x'],
                'y': rect['y'] + rect['height'],
                'width': free_rect['width'],
                'height': new_height
            }
            self.free_rectangles.append(new_rect)

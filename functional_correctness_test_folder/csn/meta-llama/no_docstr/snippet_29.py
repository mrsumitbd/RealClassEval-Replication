
class RectangleBin:
    def __init__(self, bounds):
        self.bounds = bounds
        self.free_regions = [bounds]

    @property
    def extents(self):
        return self.bounds

    def insert(self, size, rotate=True):
        for region in self.free_regions[:]:
            if self._fits_in_region(region, size, rotate):
                x, y, w, h = region
                self.free_regions.remove(region)
                self.free_regions.extend(self._split_region(x, y, w, h, size))
                return (x, y)
        return None

    def _fits_in_region(self, region, size, rotate):
        w, h = size
        region_w, region_h = region[2], region[3]
        return (w <= region_w and h <= region_h) or (rotate and h <= region_w and w <= region_h)

    def _split_region(self, x, y, w, h, size):
        regions = []
        rect_w, rect_h = size
        if w >= rect_w and h >= rect_h:
            if w > rect_w:
                regions.append((x + rect_w, y, w - rect_w, h))
            if h > rect_h:
                regions.append((x, y + rect_h, w, h - rect_h))
        else:
            rect_w, rect_h = rect_h, rect_w
            if w > rect_w:
                regions.append((x + rect_w, y, w - rect_w, h))
            if h > rect_h:
                regions.append((x, y + rect_h, w, h - rect_h))
        regions = [(r[0], r[1], r[2], r[3])
                   for r in regions if r[2] > 0 and r[3] > 0]
        return regions


# Example usage:
if __name__ == "__main__":
    bin = RectangleBin((0, 0, 10, 10))
    print(bin.insert((2, 3)))  # Output: (0, 0)
    print(bin.insert((4, 5)))  # Output: (2, 0)
    print(bin.extents)  # Output: (0, 0, 10, 10)

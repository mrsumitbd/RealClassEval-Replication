
class RectangleBin:

    def __init__(self, bounds):
        self.width, self.height = bounds
        self.free_rects = [(0, 0, self.width, self.height)]
        self.used_rects = []

    @property
    def extents(self):
        return (self.width, self.height)

    def insert(self, size, rotate=True):
        w, h = size
        best_rect = None
        best_index = -1
        best_score = None
        rotated = False

        for idx, (fx, fy, fw, fh) in enumerate(self.free_rects):
            for rot in ([False, True] if rotate and w != h else [False]):
                rw, rh = (h, w) if rot else (w, h)
                if rw <= fw and rh <= fh:
                    score = (fw * fh) - (rw * rh)
                    if best_score is None or score < best_score:
                        best_score = score
                        best_rect = (fx, fy, rw, rh)
                        best_index = idx
                        rotated = rot

        if best_rect is None:
            return None

        x, y, rw, rh = best_rect
        self.used_rects.append((x, y, rw, rh))

        fx, fy, fw, fh = self.free_rects.pop(best_index)

        # Split the free rectangle into up to 2 new free rectangles
        right = (x + rw, y, fx + fw - (x + rw), rh)
        below = (x, y + rh, rw, fy + fh - (y + rh))

        new_free = []
        if right[2] > 0 and right[3] > 0:
            new_free.append(right)
        if below[2] > 0 and below[3] > 0:
            new_free.append(below)
        # Remaining space to the left
        left = (fx, fy, x - fx, fh)
        if left[2] > 0 and left[3] > 0:
            new_free.append(left)
        # Remaining space above
        above = (fx, fy, fw, y - fy)
        if above[2] > 0 and above[3] > 0:
            new_free.append(above)

        self.free_rects.extend(new_free)
        self._prune_free_rects()
        return (x, y, rw, rh) if not rotated else (x, y, rh, rw)

    def _prune_free_rects(self):
        pruned = []
        for i, r in enumerate(self.free_rects):
            contained = False
            for j, s in enumerate(self.free_rects):
                if i != j and self._is_contained_in(r, s):
                    contained = True
                    break
            if not contained:
                pruned.append(r)
        self.free_rects = pruned

    def _is_contained_in(self, r, s):
        rx, ry, rw, rh = r
        sx, sy, sw, sh = s
        return (rx >= sx and ry >= sy and
                rx + rw <= sx + sw and
                ry + rh <= sy + sh)

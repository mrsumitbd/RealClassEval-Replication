class RectangleBin:

    def __init__(self, bounds):
        if len(bounds) != 2 or bounds[0] <= 0 or bounds[1] <= 0:
            raise ValueError(
                "bounds must be a tuple (width, height) with positive values")
        self.width, self.height = int(bounds[0]), int(bounds[1])
        self._free = [(0, 0, self.width, self.height)]
        self._used = []
        self._max_x = 0
        self._max_y = 0

    @property
    def extents(self):
        return (self._max_x, self._max_y)

    def insert(self, size, rotate=True):
        if len(size) != 2 or size[0] <= 0 or size[1] <= 0:
            raise ValueError(
                "size must be a tuple (width, height) with positive values")
        w_req, h_req = int(size[0]), int(size[1])

        candidates = []
        for idx, fr in enumerate(self._free):
            fx, fy, fw, fh = fr
            # Try without rotation
            if w_req <= fw and h_req <= fh:
                candidates.append((idx, False, fx, fy, w_req,
                                  h_req, fw * fh - w_req * h_req))
            # Try with rotation
            if rotate and h_req <= fw and w_req <= fh:
                candidates.append(
                    (idx, True, fx, fy, h_req, w_req, fw * fh - w_req * h_req))

        if not candidates:
            return None

        # Choose the candidate with smallest area waste, tie-break by y then x (top-left heuristic)
        candidates.sort(key=lambda c: (c[6], c[3], c[2]))
        idx, rotated, px, py, pw, ph, _ = candidates[0]

        placed = (px, py, pw, ph)
        self._place_and_update(placed)

        self._max_x = max(self._max_x, px + pw)
        self._max_y = max(self._max_y, py + ph)
        self._used.append(placed)

        return placed

    # Internal helpers
    def _place_and_update(self, rect):
        # Subtract the placed rect from all free rectangles and rebuild the free list
        new_free = []
        for fr in self._free:
            new_free.extend(self._subtract_rect(fr, rect))

        # Prune redundant rectangles (remove those fully contained in another)
        pruned = self._prune_contained(new_free)

        # Optionally, we could merge adjacent rectangles, but pruning is sufficient for correctness
        self._free = pruned

    @staticmethod
    def _intersect(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        ix = max(ax, bx)
        iy = max(ay, by)
        ix2 = min(ax + aw, bx + bw)
        iy2 = min(ay + ah, by + bh)
        if ix < ix2 and iy < iy2:
            return (ix, iy, ix2 - ix, iy2 - iy)
        return None

    @staticmethod
    def _subtract_rect(free_rect, used_rect):
        # Returns a list of rectangles representing free_rect minus used_rect
        fx, fy, fw, fh = free_rect
        ux, uy, uw, uh = used_rect

        inter = RectangleBin._intersect(free_rect, used_rect)
        if inter is None:
            return [free_rect]

        ix, iy, iw, ih = inter
        result = []

        # Left side
        if ix > fx:
            result.append((fx, fy, ix - fx, fh))
        # Right side
        right_x = ix + iw
        fr_right = fx + fw
        if right_x < fr_right:
            result.append((right_x, fy, fr_right - right_x, fh))
        # Top side
        if iy > fy:
            top_h = iy - fy
            # The middle strip that remains above the intersection, constrained to intersection's horizontal span
            result.append((ix, fy, iw, top_h))
        # Bottom side
        bottom_y = iy + ih
        fr_bottom = fy + fh
        if bottom_y < fr_bottom:
            bottom_h = fr_bottom - bottom_y
            result.append((ix, bottom_y, iw, bottom_h))

        # Filter zero-area
        result = [r for r in result if r[2] > 0 and r[3] > 0]
        return result

    @staticmethod
    def _contains(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax <= bx and ay <= by and (ax + aw) >= (bx + bw) and (ay + ah) >= (by + bh)

    @staticmethod
    def _prune_contained(rects):
        # Remove rectangles that are fully contained within another
        pruned = []
        for i, r in enumerate(rects):
            contained = False
            for j, s in enumerate(rects):
                if i != j and RectangleBin._contains(s, r):
                    contained = True
                    break
            if not contained:
                pruned.append(r)
        return pruned

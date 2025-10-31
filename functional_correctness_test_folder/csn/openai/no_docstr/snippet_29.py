
class RectangleBin:
    """
    A very simple rectangle bin packing implementation.
    The bin is defined by its bounds (width, height). Rectangles are inserted
    into the bin using a naive free‑space splitting strategy.
    """

    def __init__(self, bounds):
        """
        Create a new bin.

        Parameters
        ----------
        bounds : tuple
            (width, height) of the bin.
        """
        self.width, self.height = bounds
        # List of free rectangles: each is (x, y, w, h)
        self._free = [(0, 0, self.width, self.height)]
        # List of placed rectangles: each is (x, y, w, h)
        self._placed = []

    @property
    def extents(self):
        """
        Return the current extents of the placed rectangles as
        (max_x, max_y). If nothing is placed, returns (0, 0).
        """
        if not self._placed:
            return (0, 0)
        max_x = max(x + w for (x, y, w, h) in self._placed)
        max_y = max(y + h for (x, y, w, h) in self._placed)
        return (max_x, max_y)

    def insert(self, size, rotate=True):
        """
        Insert a rectangle into the bin.

        Parameters
        ----------
        size : tuple
            (width, height) of the rectangle to insert.
        rotate : bool, optional
            If True, the rectangle may be rotated 90 degrees.

        Returns
        -------
        tuple or None
            (x, y) coordinates of the bottom‑left corner where the rectangle
            was placed, or None if the rectangle could not be placed.
        """
        w, h = size
        candidates = [(w, h)]
        if rotate and w != h:
            candidates.append((h, w))

        for pw, ph in candidates:
            for i, (fx, fy, fw, fh) in enumerate(self._free):
                if pw <= fw and ph <= fh:
                    # Place rectangle at the bottom‑left of this free rect
                    x, y = fx, fy
                    self._placed.append((x, y, pw, ph))

                    # Split the free rect into up to two new free rects
                    new_free = []
                    # Right side
                    if fw - pw > 0:
                        new_free.append((fx + pw, fy, fw - pw, ph))
                    # Top side
                    if fh - ph > 0:
                        new_free.append((fx, fy + ph, fw, fh - ph))

                    # Replace the used free rect with the new ones
                    self._free.pop(i)
                    self._free.extend(new_free)

                    # Optional: merge free rects (not implemented for simplicity)
                    return (x, y)

        # No suitable free rect found
        return None

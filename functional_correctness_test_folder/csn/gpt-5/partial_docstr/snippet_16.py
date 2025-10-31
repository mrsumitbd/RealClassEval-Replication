class _Trail:
    '''
    Track a single trail  for a falling character effect (a la Matrix).
    '''

    def __init__(self, screen, x: int):
        self.screen = screen
        self.x = int(x)

        # Determine screen height as flexibly as possible
        height = None
        for getter in (
            lambda s: getattr(s, "height"),
            lambda s: getattr(s, "rows"),
            lambda s: s.get_height(),
            lambda s: s.getmaxyx()[0],
        ):
            try:
                height = getter(screen)
                if isinstance(height, int) and height > 0:
                    break
            except Exception:
                continue
        if not isinstance(height, int) or height <= 0:
            height = 24
        self.height = height

        # Characters and RNG
        self._chars = "01abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        try:
            import random as _random
        except Exception:  # pragma: no cover
            _random = None
        self._random = _random

        # Trail state
        self.length = self._randint(6, max(8, self.height // 2))
        self.y = -self._randint(0, self.height)  # start off-screen above
        self.speed = 1  # cells per update
        self._last_drawn = []

    def _randint(self, a: int, b: int) -> int:
        if self._random is None:
            # fallback deterministic
            return (a + b) // 2
        return self._random.randint(a, b)

    def _choice(self, seq):
        if self._random is None:
            return seq[0]
        return self._random.choice(seq)

    def _maybe_reseed(self, normal: bool):
        # normal indicates whether we are in the normal reseed cycle
        # Reseed if trail fully past bottom, or with a small random chance
        should = False
        if normal:
            if self.y - self.length > self.height:
                should = True
            else:
                # small chance to refresh variety
                if self._random and self._random.random() < 0.005:
                    should = True
        else:
            should = True

        if should:
            self.length = self._randint(6, max(8, self.height // 2))
            self.y = -self._randint(0, self.height)
            self.speed = 1
            return True
        return False

    def _draw_cell(self, x: int, y: int, ch: str, head: bool):
        # Try a variety of possible screen APIs
        s = self.screen
        # Prefer curses-like addch(y, x, ch)
        try:
            if hasattr(s, "addch"):
                return s.addch(y, x, ch)
        except Exception:
            pass
        # Generic draw(x, y, ch)
        try:
            if hasattr(s, "draw"):
                return s.draw(x, y, ch)
        except Exception:
            pass
        # set_cell(x, y, ch)
        try:
            if hasattr(s, "set_cell"):
                return s.set_cell(x, y, ch)
        except Exception:
            pass
        # putch(x, y, ch)
        try:
            if hasattr(s, "putch"):
                return s.putch(x, y, ch)
        except Exception:
            pass
        # write_at(x, y, ch)
        try:
            if hasattr(s, "write_at"):
                return s.write_at(x, y, ch)
        except Exception:
            pass
        # set(x, y, ch)
        try:
            if hasattr(s, "set"):
                return s.set(x, y, ch)
        except Exception:
            pass
        # put(x, y, ch)
        try:
            if hasattr(s, "put"):
                return s.put(x, y, ch)
        except Exception:
            pass
        # If none available, just record the last drawn for external consumption
        self._last_drawn.append((x, y, ch, head))

    def update(self, reseed: bool):
        '''
        Update that trail!
        :param reseed: Whether we are in the normal reseed cycle or not.
        '''
        self._last_drawn = []
        self._maybe_reseed(bool(reseed))

        # Advance head
        self.y += self.speed

        # Draw visible part of the trail
        head_ch = self._choice(self._chars)
        for i in range(self.length):
            yy = self.y - i
            if 0 <= yy < self.height:
                ch = head_ch if i == 0 else self._choice(self._chars)
                self._draw_cell(self.x, yy, ch, head=(i == 0))

        # Optionally return what was drawn for screens that don't implement drawing
        return list(self._last_drawn) if self._last_drawn else None

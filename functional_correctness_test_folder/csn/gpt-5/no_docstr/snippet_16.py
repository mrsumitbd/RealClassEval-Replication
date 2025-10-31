class _Trail:

    def __init__(self, screen, x: int):
        import random
        import time

        self.screen = screen
        self.x = x

        # Determine screen height as best-effort
        self.height = (
            getattr(screen, "height", None)
            or getattr(screen, "rows", None)
            or getattr(screen, "nrows", None)
        )
        if self.height is None:
            get_h = getattr(screen, "get_height", None)
            if callable(get_h):
                try:
                    self.height = int(get_h())
                except Exception:
                    self.height = 24
            else:
                self.height = 24

        # Random generator and initial state
        self._rnd = random.Random()
        self._rnd.seed((int(time.time() * 1000) ^ (x << 8)) & 0xFFFFFFFF)

        self._min_len = 4
        self._max_len = max(6, self.height // 2)
        self._chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@#$%^&*+=-"
        self._tick = 0
        self._speed = 1  # steps per move (lower = faster)
        self._move_counter = 0

        # Trail state: y positions (head at end), and current head y
        self._length = self._rnd.randint(self._min_len, self._max_len)
        # Start above the screen so it drops in
        self._head_y = -self._rnd.randint(0, self.height)
        self._positions = []  # list of y positions making up the trail
        self._last_ops = []   # last draw operations emitted

        # Initial random speed
        self._speed = self._rnd.randint(1, 3)

    def _maybe_reseed(self, normal: bool):
        # Reseed if forced or with a small probability when normal
        force = not normal
        do_reseed = force or (self._rnd.random() < 0.02)

        # Also reseed if the entire trail has moved well past the screen
        if not do_reseed:
            if self._head_y - self._length > self.height + 5:
                do_reseed = True

        if not do_reseed:
            return

        # Reset trail parameters
        self._length = self._rnd.randint(self._min_len, self._max_len)
        self._speed = self._rnd.randint(1, 3)
        self._head_y = -self._rnd.randint(0, self.height)
        self._positions = []
        self._tick = 0
        self._move_counter = 0

    def update(self, reseed: bool):
        # Optionally reseed before update
        self._maybe_reseed(normal=not reseed)

        self._tick += 1
        moved = False
        if self._tick >= self._speed:
            self._tick = 0
            moved = True

        # (y, x, char, brightness) where brightness in {'head','body','fade','clear'}
        ops = []

        if moved:
            # Move head down by one
            self._head_y += 1
            # Add new head
            self._positions.append(self._head_y)
            # Trim tail
            while len(self._positions) > self._length:
                tail_y = self._positions.pop(0)
                if 0 <= tail_y < self.height:
                    ops.append((tail_y, self.x, " ", "clear"))

        # Emit draw ops for visible positions
        for idx, y in enumerate(self._positions):
            if 0 <= y < self.height:
                # Determine brightness: head brighter
                if idx == len(self._positions) - 1:
                    brightness = "head"
                elif idx >= len(self._positions) - 3:
                    brightness = "body"
                else:
                    brightness = "fade"
                ch = self._rnd.choice(self._chars)
                ops.append((y, self.x, ch, brightness))

        self._last_ops = ops
        return ops

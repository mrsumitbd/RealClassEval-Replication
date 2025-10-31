import math
import random
from typing import Any


class _Flake:
    def __init__(self, screen: Any):
        self._screen = screen
        self.x = 0.0
        self.y = 0.0
        self.vy = 0.0
        self._phase = 0.0
        self._phase_step = 0.0
        self.char = "*"
        self._reseed()

    def _reseed(self):
        width = getattr(self._screen, "width", getattr(
            self._screen, "columns", 0)) or 0
        height = getattr(self._screen, "height",
                         getattr(self._screen, "rows", 0)) or 0

        if width <= 0:
            self.x = 0.0
        else:
            self.x = float(random.randint(0, max(0, width - 1)))

        # Start above the top of the screen
        start_span = max(1, height) if height else 1
        self.y = float(-random.randint(1, start_span))
        self.vy = random.uniform(0.35, 1.25)

        self.char = random.choice(("*", "•", "·", "❄"))
        self._phase = random.uniform(0.0, 2.0 * math.pi)
        self._phase_step = random.uniform(0.03, 0.12)

    def update(self, reseed: bool):
        width = getattr(self._screen, "width", getattr(
            self._screen, "columns", 0)) or 0
        height = getattr(self._screen, "height",
                         getattr(self._screen, "rows", 0)) or 0

        # Horizontal drift (sway)
        if width > 0:
            drift_amplitude = max(0.0, min(1.5, width * 0.02))
            self.x += math.sin(self._phase) * 0.25 * drift_amplitude
            self._phase += self._phase_step
            if self._phase > 2.0 * math.pi:
                self._phase -= 2.0 * math.pi

            # Clamp to screen bounds
            if self.x < 0.0:
                self.x = 0.0
            elif self.x > width - 1:
                self.x = float(width - 1)

        # Fall
        self.y += self.vy

        # If out of bounds at bottom, reseed or pin to bottom
        if height > 0 and self.y >= height:
            if reseed:
                self._reseed()
            else:
                self.y = float(height - 1)
                self.vy = 0.0

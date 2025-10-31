class Increaser:

    def __init__(self, value_range: tuple[float, float] | None):
        self._value_range: tuple[float, float] | None = value_range
        self._current: float | None = value_range[0] if value_range is not None else None

    @property
    def current(self) -> float | None:
        return self._current

    def increase(self):
        if self._value_range is None:
            return
        _, end_value = self._value_range
        self._current = self._current + 0.5 * (end_value - self._current)
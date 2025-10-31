class Clock:
    def __init__(self) -> None:
        self._now_ns = 0

    def update(self, ns: int) -> None:
        self._now_ns += ns

    @property
    def now_ns(self) -> int:
        return self._now_ns

    @property
    def now_s(self) -> float:
        return self._now_ns / 1_000_000_000.0

class Clock:

    def __init__(self) -> None:
        self._ns: int = 0

    def update(self, ns: int) -> None:
        if not isinstance(ns, int):
            raise TypeError("ns must be an integer number of nanoseconds")
        if ns < 0:
            raise ValueError("ns must be non-negative")
        self._ns += ns

    @property
    def now_ns(self) -> int:
        return self._ns

    @property
    def now_s(self) -> float:
        return self._ns / 1_000_000_000.0

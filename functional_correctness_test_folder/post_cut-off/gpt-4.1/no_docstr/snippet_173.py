
class Clock:

    def __init__(self) -> None:
        self._ns = 0

    def update(self, ns: int) -> None:
        self._ns += ns

    @property
    def now_ns(self) -> int:
        return self._ns

    @property
    def now_s(self) -> float:
        return self._ns / 1_000_000_000

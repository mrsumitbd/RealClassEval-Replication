
class Clock:

    def __init__(self) -> None:
        self._time_ns = 0

    def update(self, ns: int) -> None:
        self._time_ns += ns

    @property
    def now_ns(self) -> int:
        return self._time_ns

    @property
    def now_s(self) -> float:
        return self._time_ns / 1e9

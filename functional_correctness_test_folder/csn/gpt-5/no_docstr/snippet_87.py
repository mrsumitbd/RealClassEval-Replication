class ContextFlag:

    def __init__(self) -> None:
        self._depth = 0

    def __bool__(self) -> bool:
        return self._depth > 0

    def __enter__(self) -> None:
        self._depth += 1
        return None

    def __exit__(self, *args: object) -> None:
        if self._depth > 0:
            self._depth -= 1
        return None

class ContextFlag:
    def __init__(self) -> None:
        self._counter = 0

    def __bool__(self) -> bool:
        return self._counter > 0

    def __enter__(self) -> None:
        self._counter += 1
        return None

    def __exit__(self, *args: object) -> None:
        if self._counter > 0:
            self._counter -= 1
        else:
            self._counter = 0
        return None

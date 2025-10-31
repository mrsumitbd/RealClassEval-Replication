
class ContextFlag:

    def __init__(self) -> None:
        self._flag = False

    def __bool__(self) -> bool:
        return self._flag

    def __enter__(self) -> None:
        self._flag = True

    def __exit__(self, *args: object) -> None:
        self._flag = False


class ContextFlag:

    def __init__(self) -> None:
        self._active = False

    def __bool__(self) -> bool:
        return self._active

    def __enter__(self) -> None:
        self._active = True

    def __exit__(self, *args: object) -> None:
        self._active = False

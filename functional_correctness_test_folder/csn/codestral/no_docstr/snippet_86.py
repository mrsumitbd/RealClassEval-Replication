
class Cmd2AttributeWrapper:

    def __init__(self, attribute: Any) -> None:
        self._attribute = attribute

    def get(self) -> Any:
        return self._attribute

    def set(self, new_val: Any) -> None:
        self._attribute = new_val

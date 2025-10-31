
class Immutable:

    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(
            "Cannot modify attributes of an Immutable instance")

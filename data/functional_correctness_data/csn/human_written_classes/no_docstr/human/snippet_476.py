class SignedValue:

    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return str(self.value)
        return ''
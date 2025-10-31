class ErrorResult:
    """Simple error result class."""

    def to_text(self) -> str:
        return self.value

    def __init__(self, message: str):
        self.value = message
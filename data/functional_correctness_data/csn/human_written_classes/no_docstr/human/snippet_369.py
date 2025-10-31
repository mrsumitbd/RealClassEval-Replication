class DummyColor:

    def __call__(self, text: str):
        return text

    def __repr__(self) -> str:
        return 'DummyColor()'
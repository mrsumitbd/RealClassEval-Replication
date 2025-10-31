
class _FakeParent:

    def __init__(self, element: 'bs4.Tag') -> None:
        self.element = element

    def __len__(self) -> int:
        return len(self.element.contents)

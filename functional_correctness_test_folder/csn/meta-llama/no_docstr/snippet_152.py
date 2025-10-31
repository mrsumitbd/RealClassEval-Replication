
import bs4


class _FakeParent:

    def __init__(self, element: bs4.Tag) -> None:
        self.element = element
        self.contents = list(element.contents)

    def __len__(self) -> int:
        return len(self.contents)


from bs4 import Tag


class _FakeParent:

    def __init__(self, element: Tag) -> None:
        self.element = element
        self.children = list(element.children)

    def __len__(self) -> int:
        return len(self.children)


import bs4


class _FakeParent:
    """
    A lightweight wrapper around a BeautifulSoup Tag that behaves like a container.
    """

    def __init__(self, element: bs4.Tag) -> None:
        if not isinstance(element, bs4.Tag):
            raise TypeError("element must be a bs4.Tag instance")
        self.element = element

    def __len__(self) -> int:
        """
        Return the number of direct children of the wrapped Tag.
        """
        return len(self.element)

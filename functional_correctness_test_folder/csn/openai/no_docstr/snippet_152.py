
import bs4


class _FakeParent:
    """
    A lightweight wrapper around a BeautifulSoup Tag that mimics the
    behaviour of a parent container for the purposes of length checks.
    """

    def __init__(self, element: bs4.Tag) -> None:
        """
        Store the provided BeautifulSoup Tag.

        Parameters
        ----------
        element : bs4.Tag
            The tag to wrap.
        """
        self.element = element

    def __len__(self) -> int:
        """
        Return the number of children of the wrapped tag.

        Returns
        -------
        int
            The number of child nodes in the tag.
        """
        # BeautifulSoup's Tag implements __len__ to return the number of
        # children, so we delegate to it.
        return len(self.element)

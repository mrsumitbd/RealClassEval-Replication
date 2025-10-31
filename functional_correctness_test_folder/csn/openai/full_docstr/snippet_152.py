
import bs4


class _FakeParent:
    '''
    Fake parent class.
    When we have a fragment with no `BeautifulSoup` document object,
    we can't evaluate `nth` selectors properly.  Create a temporary
    fake parent so we can traverse the root element as a child.
    '''

    def __init__(self, element: bs4.Tag) -> None:
        '''Initialize.'''
        self.element = element
        # Provide a minimal interface that BeautifulSoup expects
        # for a parent tag: a `contents` list containing the element.
        self.contents = [element]

    def __len__(self) -> int:
        '''Length.'''
        return len(self.contents)

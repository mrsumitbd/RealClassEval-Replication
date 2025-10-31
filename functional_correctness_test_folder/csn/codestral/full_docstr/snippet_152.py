
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

    def __len__(self) -> int:
        '''Length.'''
        return 1

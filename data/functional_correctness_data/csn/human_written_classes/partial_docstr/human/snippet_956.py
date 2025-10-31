from collections import OrderedDict

class DefaultContextLocator:
    """
    One-to-one mapping between contexts and trackers.  Every tracker will
    get a new context instance and it will always be returned by this
    locator.
    """

    def __init__(self):
        self.context = OrderedDict()

    def get(self):
        """Get a reference to the context."""
        return self.context
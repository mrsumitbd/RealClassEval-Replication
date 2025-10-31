class InactiveDueCreditCollector:
    """Just a stub at the Collector which would not do anything"""

    def _donothing(self, *args, **kwargs):
        """Perform no good and no bad"""
        pass

    def dcite(self, *args, **kwargs):
        """If I could cite I would"""

        def nondecorating_decorator(func):
            return func
        return nondecorating_decorator
    active = False
    activate = add = cite = dump = load = _donothing

    def __repr__(self):
        return self.__class__.__name__ + '()'
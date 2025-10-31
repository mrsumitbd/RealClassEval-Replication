class FeedbackComponent:

    def __init__(self, message: str, kwargs: dict=None, append=True):
        self.message = message
        self.kwargs = kwargs or {}
        self.append = append

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, repr(vars(self)))
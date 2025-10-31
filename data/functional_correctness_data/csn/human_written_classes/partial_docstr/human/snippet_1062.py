class DrmaaSessionFactory:
    """
    Abstraction used to production DrmaaSession wrappers.
    """

    def __init__(self):
        self.session_constructor = Session

    def get(self, **kwds):
        session_constructor = self.session_constructor
        if session_constructor is None:
            raise Exception(NO_DRMAA_MESSAGE + LOAD_ERROR_MESSAGE)
        return DrmaaSession(session_constructor, **kwds)
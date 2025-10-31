class SessionHandler:
    """ Set the stage for a handler with session. The session per-se will be
    managed by the ComponentHandler that extends SessionHandler.
    """

    def __init__(self):
        self.session = None
        self.skip_auth = False

    def authenticated(self):
        """ Returns if the current user is authenticated. If the current user
        is set then we consider authenticated.

        :return: bool True is current user is set
        """
        return self.current_user is not None
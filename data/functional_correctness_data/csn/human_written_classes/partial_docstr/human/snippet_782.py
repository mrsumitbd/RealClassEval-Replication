class Status:
    """
    By default, the agent's local region is used

    https://www.nomadproject.io/docs/http/status.html
    """

    def __init__(self, **kwargs):
        self.leader = Leader(**kwargs)
        self.peers = Peers(**kwargs)

    def __str__(self):
        return f'{self.__dict__}'

    def __repr__(self):
        return f'{self.__dict__}'

    def __getattr__(self, item):
        msg = f'{item} does not exist'
        raise AttributeError(msg)
class Event:
    """
    Nomad Event
    """

    def __str__(self):
        return f'{self.__dict__}'

    def __repr__(self):
        return f'{self.__dict__}'

    def __getattr__(self, item):
        raise AttributeError

    def __init__(self, **kwargs):
        self.stream = stream(**kwargs)
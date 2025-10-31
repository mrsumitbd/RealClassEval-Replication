class Client:
    """
    The /client endpoints are used to interact with the Nomad clients.
    """

    def __init__(self, **kwargs):
        self.ls = ls(**kwargs)
        self.cat = cat(**kwargs)
        self.stat = stat(**kwargs)
        self.stats = stats(**kwargs)
        self.allocation = allocation(**kwargs)
        self.read_at = read_at(**kwargs)
        self.stream_file = stream_file(**kwargs)
        self.stream_logs = stream_logs(**kwargs)
        self.gc_allocation = gc_allocation(**kwargs)
        self.gc_all_allocations = gc_all_allocations(**kwargs)

    def __str__(self):
        return f'{self.__dict__}'

    def __repr__(self):
        return f'{self.__dict__}'

    def __getattr__(self, item):
        msg = f'{item} does not exist'
        raise AttributeError(msg)
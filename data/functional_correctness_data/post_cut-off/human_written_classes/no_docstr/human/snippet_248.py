class _InternalDataLoader:

    def __init__(self, config):
        self.config = config
        self.dataset = None
        self.index = 0
        self.experience_buffer = None

    def state_dict(self):
        return None

    def load_state_dict(self, *args, **kwargs):
        pass

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        raise StopIteration
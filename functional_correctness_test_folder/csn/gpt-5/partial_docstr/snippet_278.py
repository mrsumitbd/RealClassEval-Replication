class Dumper:
    '''Interface for dumpers.'''

    def dump(self, record, data):
        raise NotImplementedError("dump must be implemented by subclasses")

    def load(self, data, record_cls):
        raise NotImplementedError("load must be implemented by subclasses")

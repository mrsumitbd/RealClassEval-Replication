
class Dumper:
    '''Interface for dumpers.'''

    def dump(self, record, data):
        raise NotImplementedError("Subclasses must implement this method")

    def load(self, data, record_cls):
        raise NotImplementedError("Subclasses must implement this method")

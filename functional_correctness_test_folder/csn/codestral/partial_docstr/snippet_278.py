
class Dumper:
    '''Interface for dumpers.'''

    def dump(self, record, data):
        pass

    def load(self, data, record_cls):
        pass

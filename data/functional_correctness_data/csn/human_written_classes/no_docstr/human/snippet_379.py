class DummyMatch:

    def __init__(self, string):
        self.string = string

    def group(self, index):
        if index == 0:
            return self.string
        raise IndexError('no such group')

    @staticmethod
    def groupdict(*arg, **kwargs):
        return {}
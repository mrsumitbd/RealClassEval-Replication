class MissingKey:

    def __init__(self, elem):
        self.elem = elem

    def __repr__(self):
        return '<{} elem={}>'.format(self.__class__.__name__, self.elem)
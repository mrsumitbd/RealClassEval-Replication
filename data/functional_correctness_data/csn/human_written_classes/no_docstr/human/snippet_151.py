class Shape:

    def __init__(self, tokens):
        self.__dict__.update(tokens.asDict())

    def area(self):
        raise NotImplemented()

    def __str__(self):
        return '<{}>: {}'.format(self.__class__.__name__, vars(self))
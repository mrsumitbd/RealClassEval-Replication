class Subroutine:

    def __init__(self):
        self.index = None
        self.name = None
        self.extra = None

    def __repr__(self):
        return f'<Subroutine: {self.index}>'

    @property
    def mglo(self):
        return self
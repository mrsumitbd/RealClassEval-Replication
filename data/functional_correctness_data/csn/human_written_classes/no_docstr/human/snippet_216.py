class Varying:

    def __init__(self):
        self.number = None
        self.array_length = None
        self.dimension = None
        self.name = None
        self.extra = None

    def __repr__(self):
        return f'<Varying: {self.number}>'

    @property
    def mglo(self):
        return self
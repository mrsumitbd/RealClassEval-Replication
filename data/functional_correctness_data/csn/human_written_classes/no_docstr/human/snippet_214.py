class Attribute:

    def __init__(self):
        self.gl_type = None
        self.program_obj = None
        self.scalar_type = None
        self.rows_length = None
        self.row_length = None
        self.normalizable = None
        self.location = None
        self.array_length = None
        self.dimension = None
        self.shape = None
        self.name = None
        self.extra = None

    def __repr__(self):
        return f'<Attribute: {self.location}>'

    @property
    def mglo(self):
        return self
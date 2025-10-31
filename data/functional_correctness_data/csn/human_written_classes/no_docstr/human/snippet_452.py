class TraversedRelationship:
    __slots__ = ['from_model', 'field']

    def __init__(self, from_model, field):
        self.from_model = from_model
        self.field = field

    @property
    def field_name(self) -> str:
        return self.field.name

    @property
    def to_model(self):
        return self.field.target_model
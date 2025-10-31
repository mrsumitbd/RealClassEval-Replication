class Charset:

    def __init__(self, id, name, collation, is_default=False):
        self.id, self.name, self.collation = (id, name, collation)
        self.is_default = is_default

    def __repr__(self):
        return f'Charset(id={self.id}, name={self.name!r}, collation={self.collation!r})'

    @property
    def encoding(self):
        name = self.name
        if name in ('utf8mb4', 'utf8mb3'):
            return 'utf8'
        if name == 'latin1':
            return 'cp1252'
        if name == 'koi8r':
            return 'koi8_r'
        if name == 'koi8u':
            return 'koi8_u'
        return name

    @property
    def is_binary(self):
        return self.id == 63
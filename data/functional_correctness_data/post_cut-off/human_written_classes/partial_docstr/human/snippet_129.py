class Schema:
    """
    Simple schema which maps table&column to a unique identifier
    """

    def __init__(self, schema):
        self._schema = schema
        self._idMap = self._map(self._schema)

    @property
    def schema(self):
        return self._schema

    @property
    def idMap(self):
        return self._idMap

    def _map(self, schema):
        idMap = {'*': '__all__'}
        id = 1
        for key, vals in schema.items():
            for val in vals:
                idMap[key.lower() + '.' + val.lower()] = '__' + key.lower() + '.' + val.lower() + '__'
                id += 1
        for key in schema:
            idMap[key.lower()] = '__' + key.lower() + '__'
            id += 1
        return idMap
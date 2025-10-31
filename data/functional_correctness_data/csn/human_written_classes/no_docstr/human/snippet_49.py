class Box:
    type_mappings = {}
    types = set()
    __slots__ = ['_value', '_trace', '_node']

    def __init__(self, value, trace, node):
        self._value = value
        self._node = node
        self._trace = trace

    def __bool__(self):
        return bool(self._value)
    __nonzero__ = __bool__

    def __str__(self):
        return f'Autograd {type(self).__name__} with value {str(self._value)}'

    @classmethod
    def register(cls, value_type):
        Box.types.add(cls)
        Box.type_mappings[value_type] = cls
        Box.type_mappings[cls] = cls
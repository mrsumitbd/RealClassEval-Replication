class Variable:
    '''The representation of a variable with value and type.'''

    _TYPE_MAP = {
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
        'list': list,
        'dict': dict,
        'tuple': tuple,
        'set': set,
        'bytes': bytes,
    }

    def __init__(self, val, _type):
        '''
        :param val:
        :param _type:
        '''
        self.type = self._resolve_type(_type)
        self.value = self._coerce_value(val, self.type)

    def _resolve_type(self, _type):
        if isinstance(_type, type):
            return _type
        if isinstance(_type, str):
            t = self._TYPE_MAP.get(_type.strip().lower())
            if t is not None:
                return t
        raise TypeError("Unsupported type specification")

    def _coerce_value(self, val, tp):
        if isinstance(val, tp):
            return val
        if tp is bool:
            if isinstance(val, str):
                v = val.strip().lower()
                if v in ('true', '1', 'yes', 'y', 't'):
                    return True
                if v in ('false', '0', 'no', 'n', 'f'):
                    return False
                raise ValueError("Cannot convert string to bool")
            if isinstance(val, (int, float)):
                return bool(val)
        try:
            return tp(val)
        except Exception as e:
            raise ValueError(f"Cannot convert value to {tp.__name__}") from e

    def __str__(self):
        return f"{self.value} ({self.type.__name__})"

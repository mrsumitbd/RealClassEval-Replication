class Variable:

    def __init__(self, val, _type):
        type_map = {
            'int': int,
            'float': float,
            'str': str,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
        }

        if isinstance(_type, str):
            if _type not in type_map:
                raise TypeError(f"Unsupported type string: {_type}")
            target_type = type_map[_type]
        elif isinstance(_type, type):
            target_type = _type
        else:
            raise TypeError(
                "Type must be a type object or a supported type string")

        if target_type is bool:
            if isinstance(val, str):
                v = val.strip().lower()
                if v in ('true', '1', 'yes', 'y', 't'):
                    self.value = True
                elif v in ('false', '0', 'no', 'n', 'f'):
                    self.value = False
                else:
                    raise ValueError(f"Cannot convert string '{val}' to bool")
            else:
                self.value = bool(val)
        else:
            self.value = target_type(val)

        self.type = target_type

    def __str__(self):
        return str(self.value)

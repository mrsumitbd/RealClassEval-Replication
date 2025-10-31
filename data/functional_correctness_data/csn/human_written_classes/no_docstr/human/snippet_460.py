from copy import deepcopy

class CopyHandler:
    key = '__copy__'

    def __init__(self, configs):
        self.configs = configs

    @staticmethod
    def _resolve(configs, dotted_path):
        for config in configs[::-1]:
            value = config
            for part in dotted_path.split('.'):
                try:
                    value = value[part]
                except KeyError:
                    break
            else:
                return value
        else:
            raise KeyError(dotted_path)

    def __call__(self, name, props):
        dotted_path = props[self.key]
        try:
            value = self._resolve(self.configs[-1:], dotted_path)
            self_reference = value is props
        except KeyError:
            self_reference = False
        if self_reference:
            value = self._resolve(self.configs[:-1], dotted_path)
        else:
            try:
                value = self._resolve(self.configs, dotted_path)
            except KeyError:
                if '__default__' in props:
                    return props['__default__']
                else:
                    raise
        value = deepcopy(value)
        nonmagicprops = [prop for prop in props if not (prop.startswith('__') and prop.endswith('__'))]
        if nonmagicprops:
            recursive_copy = self.key in value
            value.update(props)
            if not recursive_copy:
                del value[self.key]
        return value
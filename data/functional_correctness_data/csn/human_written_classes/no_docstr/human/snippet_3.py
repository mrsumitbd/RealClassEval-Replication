class _BaseOptionsDescriptor:

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls):
        if self.name == 'enableBidi':
            value = obj._caps.get('webSocketUrl')
            return value is True or isinstance(value, str)
        if self.name == 'webSocketUrl':
            value = obj._caps.get(self.name)
            return None if not isinstance(value, str) else value
        if self.name in ('acceptInsecureCerts', 'strictFileInteractability', 'setWindowRect', 'se:downloadsEnabled'):
            return obj._caps.get(self.name, False)
        return obj._caps.get(self.name)

    def __set__(self, obj, value):
        if self.name == 'enableBidi':
            obj.set_capability('webSocketUrl', value)
        else:
            obj.set_capability(self.name, value)
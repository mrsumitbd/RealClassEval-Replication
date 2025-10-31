class Capability:
    """Represents a single capability"""

    def __init__(self, namespace_uri, parameters=None):
        self.namespace_uri = namespace_uri
        self.parameters = parameters or {}

    @classmethod
    def from_uri(cls, uri):
        split_uri = uri.split('?')
        namespace_uri = split_uri[0]
        capability = cls(namespace_uri)
        try:
            param_string = split_uri[1]
        except IndexError:
            return capability
        capability.parameters = {param.key: param.value for param in _parse_parameter_string(param_string, uri)}
        return capability

    def __eq__(self, other):
        return self.namespace_uri == other.namespace_uri and self.parameters == other.parameters

    def get_abbreviations(self):
        return _abbreviate(self.namespace_uri)
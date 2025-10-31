class _DeepStringCoder:
    """
    Encodes and decodes strings in a nested structure of lists, tuples, and
    dicts. This is helpful when interacting with the Unicode-unaware
    python-ldap.
    """

    def __init__(self, encoding):
        self.encoding = encoding
        self.ldap = _LDAPConfig.get_ldap()

    def decode(self, value):
        try:
            if isinstance(value, bytes):
                value = value.decode(self.encoding)
            elif isinstance(value, list):
                value = self._decode_list(value)
            elif isinstance(value, tuple):
                value = tuple(self._decode_list(value))
            elif isinstance(value, dict):
                value = self._decode_dict(value)
        except UnicodeDecodeError:
            pass
        return value

    def _decode_list(self, value):
        return [self.decode(v) for v in value]

    def _decode_dict(self, value):
        decoded = self.ldap.cidict.cidict()
        for k, v in value.items():
            decoded[self.decode(k)] = self.decode(v)
        return decoded
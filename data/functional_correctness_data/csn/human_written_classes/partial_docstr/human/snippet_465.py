from aredis.exceptions import SerializeError, CompressError

class Serializer:
    """
    Uses json to serialize and deserialize cache to str. You may implement
    your own Serializer implemting `serialize` and `deserialize` methods.
    """

    def __init__(self, encoding='utf-8'):
        self.encoding = encoding

    def _trans_type(self, content):
        if isinstance(content, bytes):
            content = content.decode(self.encoding)
        if not isinstance(content, str):
            raise TypeError('Wrong data type({}) to compress'.format(type(content)))
        return content

    def serialize(self, content):
        try:
            return json.dumps(content)
        except Exception as exc:
            raise SerializeError('Content can not be serialized.')

    def deserialize(self, content):
        content = self._trans_type(content)
        try:
            return json.loads(content)
        except Exception as exc:
            raise SerializeError('Content can not be deserialized.')
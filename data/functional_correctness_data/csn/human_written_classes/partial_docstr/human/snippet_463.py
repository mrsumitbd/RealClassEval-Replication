from aredis.utils import b
from aredis.exceptions import SerializeError, CompressError
import zlib

class Compressor:
    """
    Uses zlib to compress and decompress Redis cache. You may implement your
    own Compressor implementing `compress` and `decompress` methods
    """
    min_length = 15
    preset = 6

    def __init__(self, encoding='utf-8'):
        self.encoding = encoding

    def _trans_type(self, content):
        if isinstance(content, str):
            content = content.encode(self.encoding)
        elif isinstance(content, int):
            content = b(str(content))
        elif isinstance(content, float):
            content = b(repr(content))
        if not isinstance(content, bytes):
            raise TypeError('Wrong data type({}) to compress'.format(type(content)))
        return content

    def compress(self, content):
        content = self._trans_type(content)
        if len(content) > self.min_length:
            try:
                return zlib.compress(content, self.preset)
            except zlib.error as exc:
                raise CompressError('Content can not be compressed.')
        return content

    def decompress(self, content):
        content = self._trans_type(content)
        try:
            return zlib.decompress(content)
        except zlib.error as exc:
            raise CompressError('Content can not be decompressed.')
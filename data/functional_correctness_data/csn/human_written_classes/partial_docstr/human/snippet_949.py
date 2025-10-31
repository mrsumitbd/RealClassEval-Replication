import numpy

class GLTFBufferView:

    def __init__(self, view_id, data):
        self.id = view_id
        self.bufferId = data.get('buffer')
        self.buffer = None
        self.byteOffset = data.get('byteOffset') or 0
        self.byteLength = data.get('byteLength')
        self.byteStride = data.get('byteStride') or 0

    def read(self, byte_offset=0, dtype=None, count=0):
        data = self.buffer.read(byte_offset=byte_offset + self.byteOffset, byte_length=self.byteLength)
        vbo = numpy.frombuffer(data, count=count, dtype=dtype)
        return vbo

    def read_raw(self):
        return self.buffer.read(byte_length=self.byteLength, byte_offset=self.byteOffset)

    def info(self, byte_offset=0):
        """
        Get the underlying buffer info
        :param byte_offset: byte offset from accessor
        :return: buffer, byte_length, byte_offset
        """
        return (self.buffer, self.byteLength, byte_offset + self.byteOffset)
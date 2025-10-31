import numpy

class GLTFAccessor:

    def __init__(self, accessor_id, data):
        self.id = accessor_id
        self.bufferViewId = data.get('bufferView') or 0
        self.bufferView = None
        self.byteOffset = data.get('byteOffset') or 0
        self.componentType = COMPONENT_TYPE[data['componentType']]
        self.count = data.get('count')
        self.min = numpy.array(data.get('min') or [-0.5, -0.5, -0.5], dtype=numpy.float32)
        self.max = numpy.array(data.get('max') or [0.5, 0.5, 0.5], dtype=numpy.float32)
        self.type = data.get('type')

    def read(self):
        """
        Reads buffer data
        :return: component count, component type, data
        """
        dtype = NP_COMPONENT_DTYPE[self.componentType.value]
        return (ACCESSOR_TYPE[self.type], self.componentType, self.bufferView.read(byte_offset=self.byteOffset, dtype=dtype, count=self.count * ACCESSOR_TYPE[self.type]))

    def info(self):
        """
        Get underlying buffer info for this accessor
        :return: buffer, byte_length, byte_offset, component_type, count
        """
        buffer, byte_length, byte_offset = self.bufferView.info(byte_offset=self.byteOffset)
        return (buffer, self.bufferView, byte_length, byte_offset, self.componentType, ACCESSOR_TYPE[self.type], self.count)
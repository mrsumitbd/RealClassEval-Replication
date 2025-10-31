import struct

class RecordWriter:

    def __init__(self, path):
        self._name_to_tf_name = {}
        self._tf_names = set()
        self.path = path
        self._writer = None
        self._writer = open_file(path)

    def write(self, data):
        w = self._writer.write
        header = struct.pack('Q', len(data))
        w(header)
        w(struct.pack('I', masked_crc32c(header)))
        w(data)
        w(struct.pack('I', masked_crc32c(data)))

    def flush(self):
        self._writer.flush()

    def close(self):
        self._writer.close()
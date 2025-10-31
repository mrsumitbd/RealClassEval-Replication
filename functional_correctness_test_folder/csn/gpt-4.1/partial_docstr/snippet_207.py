
class IJavaStreamParser:
    '''
    API of the Java stream parser
    '''

    def __init__(self):
        self.stream = None

    def run(self):
        '''
        Parses the input stream
        '''
        if self.stream is None:
            raise ValueError("No input stream set")
        results = []
        while True:
            type_code = self.stream.read(1)
            if not type_code:
                break
            block_data = self._read_block_data(type_code)
            content = self._read_content(type_code, block_data)
            results.append(content)
        return results

    def dump(self, content):
        '''
        Dumps to a string the given objects
        '''
        import pprint
        return pprint.pformat(content)

    def _read_content(self, type_code, block_data, class_desc=None):
        # Dummy implementation for demonstration
        if type_code == b'\x73':  # TC_OBJECT
            return {"type": "object", "data": block_data}
        elif type_code == b'\x74':  # TC_STRING
            return {"type": "string", "data": block_data.decode('utf-8')}
        elif type_code == b'\x75':  # TC_ARRAY
            return {"type": "array", "data": list(block_data)}
        else:
            return {"type": "unknown", "data": block_data}

    def _read_block_data(self, type_code):
        # Dummy implementation: read 4 bytes for block length, then that many bytes
        import struct
        if self.stream is None:
            raise ValueError("No input stream set")
        length_bytes = self.stream.read(4)
        if len(length_bytes) < 4:
            return b''
        length = struct.unpack('>I', length_bytes)[0]
        return self.stream.read(length)

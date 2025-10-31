
import struct
from io import BytesIO


class IJavaStreamParser:
    '''
    API of the Java stream parser
    '''
    # Java serialization type codes (subset)
    TC_OBJECT = 0x70
    TC_CLASSDESC = 0x71
    TC_STRING = 0x73
    TC_LONGSTRING = 0x78
    TC_ARRAY = 0x75
    TC_CLASS = 0x76
    TC_BLOCKDATA = 0x77
    TC_ENDBLOCKDATA = 0x78
    TC_RESET = 0x79
    TC_BLOCKDATALONG = 0x7A
    TC_EXCEPTION = 0x7B
    TC_LONGSTRING = 0x7C
    TC_PROXYCLASSDESC = 0x7D
    TC_ENUM = 0x7E

    def __init__(self, stream):
        """
        Initialize the parser with a binary stream.
        """
        if isinstance(stream, (bytes, bytearray)):
            self.stream = BytesIO(stream)
        else:
            self.stream = stream
        self.objects = []

    def run(self):
        """
        Parses the input stream and populates self.objects.
        """
        while True:
            type_code_byte = self.stream.read(1)
            if not type_code_byte:
                break  # EOF
            type_code = type_code_byte[0]
            obj = self._read_content(type_code)
            if obj is not None:
                self.objects.append(obj)
        return self.objects

    def dump(self, content):
        """
        Dumps to a string the given objects.
        """
        if isinstance(content, list):
            return '\n'.join(str(o) for o in content)
        return str(content)

    def _read_content(self, type_code, class_desc=None):
        """
        Reads content based on the type code.
        """
        if type_code == self.TC_STRING:
            # Read 2-byte unsigned short length
            length_bytes = self.stream.read(2)
            if len(length_bytes) < 2:
                return None
            (length,) = struct.unpack('>H', length_bytes)
            string_bytes = self.stream.read(length)
            return string_bytes.decode('utf-8', errors='replace')
        elif type_code == self.TC_LONGSTRING:
            # Read 8-byte unsigned long length
            length_bytes = self.stream.read(8)
            if len(length_bytes) < 8:
                return None
            (length,) = struct.unpack('>Q', length_bytes)
            string_bytes = self.stream.read(length)
            return string_bytes.decode('utf-8', errors='replace')
        elif type_code == self.TC_BLOCKDATA:
            # Read 1-byte length
            length_bytes = self.stream.read(1)
            if len(length_bytes) < 1:
                return None
            (length,) = struct.unpack('>B', length_bytes)
            block = self.stream.read(length)
            return block
        elif type_code == self.TC_BLOCKDATALONG:
            # Read 4-byte length
            length_bytes = self.stream.read(4)
            if len(length_bytes) < 4:
                return None
            (length,) = struct.unpack('>I', length_bytes)
            block = self.stream.read(length)
            return block
        elif type_code == self.TC_OBJECT:
            # Skip object header for simplicity
            # Read class descriptor
            self._read_content(self.TC_CLASSDESC)
            # Skip fields (not implemented)
            return {'object': 'skipped'}
        elif type_code == self.TC_CLASSDESC:
            # Read class name string
            class_name = self._read_content(self.TC_STRING)
            # Skip serialVersionUID (8 bytes)
            self.stream.read(8)
            # Skip flags (1 byte)
            self.stream.read(1)
            # Skip field count (2 bytes)
            self.stream.read(2)
            # Skip fields (not implemented)
            return {'class': class_name}
        else:
            # Unknown or unsupported type code; skip
            return None

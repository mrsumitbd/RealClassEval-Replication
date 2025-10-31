
import struct
import io


class IJavaStreamParser:
    # Java Serialization Stream Constants
    TC_NULL = 0x70
    TC_REFERENCE = 0x71
    TC_CLASSDESC = 0x72
    TC_OBJECT = 0x73
    TC_STRING = 0x74
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

    BASE_WIRE_HANDLE = 0x7E0000

    def __init__(self):
        self.refs = {}
        self.handle_count = 0

    def run(self):
        # Example: Not implemented, as no input is provided
        pass

    def dump(self, content):
        # Pretty print the parsed content
        import pprint
        pprint.pprint(content)

    def _read_utf(self, f):
        utflen = struct.unpack('>H', f.read(2))[0]
        return f.read(utflen).decode('utf-8', errors='replace')

    def _read_long_utf(self, f):
        utflen = struct.unpack('>Q', f.read(8))[0]
        return f.read(utflen).decode('utf-8', errors='replace')

    def _new_handle(self, obj):
        handle = self.BASE_WIRE_HANDLE + self.handle_count
        self.refs[handle] = obj
        self.handle_count += 1
        return handle

    def _read_handle(self, f):
        handle = struct.unpack('>I', f.read(4))[0]
        return self.refs.get(handle, None)

    def _read_classdesc(self, f):
        class_name = self._read_utf(f)
        serial_version_uid = struct.unpack('>q', f.read(8))[0]
        classdesc_flags = struct.unpack('>B', f.read(1))[0]
        field_count = struct.unpack('>H', f.read(2))[0]
        fields = []
        for _ in range(field_count):
            typecode = f.read(1)
            field_name = self._read_utf(f)
            if typecode in b'L[':
                class_name1 = self._read_utf(f)
                fields.append((typecode, field_name, class_name1))
            else:
                fields.append((typecode, field_name))
        ann = []
        while True:
            tc = f.read(1)
            if not tc or tc[0] == self.TC_ENDBLOCKDATA:
                break
            ann.append(tc)
        super_class_desc = self._read_content(ord(f.read(1)), f)
        classdesc = {
            'type': 'classdesc',
            'name': class_name,
            'serialVersionUID': serial_version_uid,
            'flags': classdesc_flags,
            'fields': fields,
            'annotations': ann,
            'super_class_desc': super_class_desc
        }
        self._new_handle(classdesc)
        return classdesc

    def _read_string(self, f, long_string=False):
        if long_string:
            s = self._read_long_utf(f)
        else:
            s = self._read_utf(f)
        self._new_handle(s)
        return s

    def _read_array(self, f):
        class_desc = self._read_content(ord(f.read(1)), f)
        length = struct.unpack('>i', f.read(4))[0]
        arr = []
        for _ in range(length):
            arr.append(self._read_content(ord(f.read(1)), f, class_desc))
        self._new_handle(arr)
        return arr

    def _read_object(self, f):
        class_desc = self._read_content(ord(f.read(1)), f)
        obj = {'type': 'object', 'class_desc': class_desc, 'fields': {}}
        self._new_handle(obj)
        # For simplicity, skip actual field reading
        return obj

    def _read_content(self, type_code, block_data, class_desc=None):
        if isinstance(block_data, bytes):
            f = io.BytesIO(block_data)
        else:
            f = block_data

        if type_code == self.TC_NULL:
            return None
        elif type_code == self.TC_REFERENCE:
            return self._read_handle(f)
        elif type_code == self.TC_CLASSDESC:
            return self._read_classdesc(f)
        elif type_code == self.TC_OBJECT:
            return self._read_object(f)
        elif type_code == self.TC_STRING:
            return self._read_string(f)
        elif type_code == self.TC_LONGSTRING:
            return self._read_string(f, long_string=True)
        elif type_code == self.TC_ARRAY:
            return self._read_array(f)
        elif type_code == self.TC_CLASS:
            class_desc = self._read_content(ord(f.read(1)), f)
            self._new_handle(class_desc)
            return class_desc
        elif type_code == self.TC_BLOCKDATA:
            length = struct.unpack('>B', f.read(1))[0]
            data = f.read(length)
            return data
        elif type_code == self.TC_BLOCKDATALONG:
            length = struct.unpack('>I', f.read(4))[0]
            data = f.read(length)
            return data
        elif type_code == self.TC_ENDBLOCKDATA:
            return None
        else:
            return None

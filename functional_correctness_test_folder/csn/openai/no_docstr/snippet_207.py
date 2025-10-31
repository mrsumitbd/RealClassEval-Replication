
import struct
import sys
import json


class IJavaStreamParser:
    # Type codes
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

    def __init__(self, file_path):
        self.file_path = file_path
        self.objects = []

    def run(self):
        with open(self.file_path, "rb") as f:
            # Read stream header
            header = f.read(4)
            if len(header) < 4:
                raise ValueError(
                    "File too short for Java serialization header")
            magic, version = struct.unpack(">HH", header)
            if magic != 0xACED or version != 0x0005:
                raise ValueError("Not a valid Java serialization stream")
            # Parse blocks until EOF
            while True:
                type_code_raw = f.read(1)
                if not type_code_raw:
                    break  # EOF
                type_code = type_code_raw[0]
                obj = self._read_content(type_code, f)
                self.objects.append(obj)

    def dump(self, content=None):
        if content is None:
            content = self.objects
        # Pretty‑print JSON representation
        print(json.dumps(content, indent=2, default=str))

    def _read_content(self, type_code, f, class_desc=None):
        if type_code == self.TC_NULL:
            return None
        elif type_code == self.TC_REFERENCE:
            # 4-byte handle
            handle_bytes = f.read(4)
            if len(handle_bytes) < 4:
                raise ValueError(
                    "Unexpected EOF while reading reference handle")
            handle = struct.unpack(">I", handle_bytes)[0]
            return {"type": "TC_REFERENCE", "handle": handle}
        elif type_code == self.TC_CLASSDESC:
            # Read class name (TC_STRING)
            class_name = self._read_content(self.TC_STRING, f)
            # serialVersionUID (8 bytes)
            svuid_bytes = f.read(8)
            if len(svuid_bytes) < 8:
                raise ValueError(
                    "Unexpected EOF while reading serialVersionUID")
            svuid = struct.unpack(">q", svuid_bytes)[0]
            # classDescFlags (1 byte)
            flags_bytes = f.read(1)
            if len(flags_bytes) < 1:
                raise ValueError("Unexpected EOF while reading classDescFlags")
            flags = flags_bytes[0]
            # field count (2 bytes)
            field_count_bytes = f.read(2)
            if len(field_count_bytes) < 2:
                raise ValueError("Unexpected EOF while reading field count")
            field_count = struct.unpack(">H", field_count_bytes)[0]
            fields = []
            for _ in range(field_count):
                # field type code (1 byte)
                ftype = f.read(1)[0]
                # field name (TC_STRING)
                fname = self._read_content(self.TC_STRING, f)
                # field class name (TC_STRING) if type is 'L' or '['
                if chr(ftype) in ('L', '['):
                    fclass = self._read_content(self.TC_STRING, f)
                else:
                    fclass = None
                fields.append(
                    {"type": chr(ftype), "name": fname, "class": fclass})
            # class annotations (TC_BLOCKDATA until TC_ENDBLOCKDATA)
            annotations = []
            while True:
                ann_type = f.read(1)
                if not ann_type:
                    raise ValueError(
                        "Unexpected EOF while reading class annotations")
                ann_code = ann_type[0]
                if ann_code == self.TC_ENDBLOCKDATA:
                    break
                elif ann_code == self.TC_BLOCKDATA:
                    length = f.read(1)[0]
                    data = f.read(length)
                    annotations.append(data)
                else:
                    # Skip unknown annotation types
                    pass
            # super class desc
            super_desc = self._read_content(type_code, f)
            return {
                "type": "TC_CLASSDESC",
                "class_name": class_name,
                "serialVersionUID": svuid,
                "flags": flags,
                "fields": fields,
                "annotations": annotations,
                "super_desc": super_desc,
            }
        elif type_code == self.TC_OBJECT:
            # class desc
            class_desc = self._read_content(self.TC_CLASSDESC, f)
            # field values
            field_values = []
            for field in class_desc.get("fields", []):
                val = self._read_content(field.get("type", 0), f)
                field_values.append({"name": field["name"], "value": val})
            return {"type": "TC_OBJECT", "class_desc": class_desc, "fields": field_values}
        elif type_code == self.TC_STRING:
            # string length (2 bytes)
            str_len_bytes = f.read(2)
            if len(str_len_bytes) < 2:
                raise ValueError("Unexpected EOF while reading string length")
            str_len = struct.unpack(">H", str_len_bytes)[0]
            str_bytes = f.read(str_len)
            if len(str_bytes) < str_len:
                raise ValueError("Unexpected EOF while reading string data")
            return str_bytes.decode("utf-8", errors="replace")
        elif type_code == self.TC_BLOCKDATA:
            length = f.read(1)[0]
            data = f.read(length)
            if len(data) < length:
                raise ValueError("Unexpected EOF while reading blockdata")
            return {"type": "TC_BLOCKDATA",

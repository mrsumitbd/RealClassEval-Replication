class IJavaStreamParser:
    STREAM_MAGIC = 0xACED
    STREAM_VERSION = 0x0005

    # Type codes (subset)
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

    BASE_HANDLE = 0x7E0000

    def __init__(self):
        import io
        self._io = None
        self._buf = None
        self._pos = 0
        self._len = 0
        self._handles = {}
        self._next_handle = self.BASE_HANDLE
        self._io_cls = io.BytesIO

    def dump(self, content):
        import io
        import os
        if isinstance(content, (bytes, bytearray, memoryview)):
            self._buf = bytes(content)
        elif hasattr(content, "read"):
            self._buf = content.read()
        elif isinstance(content, (str, os.PathLike)):
            with open(content, "rb") as f:
                self._buf = f.read()
        else:
            raise TypeError("Unsupported content type for dump")
        self._io = self._io_cls(self._buf)
        self._pos = 0
        self._io.seek(0, 2)
        self._len = self._io.tell()
        self._io.seek(0)
        self._handles.clear()
        self._next_handle = self.BASE_HANDLE

    def run(self):
        if self._io is None:
            raise RuntimeError("No content loaded. Call dump() first.")
        # Read stream header if present
        if self._len >= 4:
            try:
                magic = self._read_u2()
                version = self._read_u2()
            except EOFError:
                return None
            if magic != self.STREAM_MAGIC or version != self.STREAM_VERSION:
                # Not a Java serialization stream; rewind and parse elements heuristically
                self._io.seek(0)
                self._pos = 0
        items = []
        while True:
            try:
                item = self._read_content_object()
            except EOFError:
                break
            if item is not _EOF:
                items.append(item)
        if not items:
            return None
        if len(items) == 1:
            return items[0]
        return items

    def _read_content(self, type_code, block_data, class_desc=None):
        # type_code: Java field type code (B C D F I J S Z L [)
        t = type_code
        if isinstance(t, bytes):
            t = t.decode("ascii", "ignore")
        if not t:
            raise ValueError("Empty type code")
        t0 = t[0]
        if t0 == "B":  # byte
            return self._read_s1()
        if t0 == "C":  # char (unsigned 2 bytes)
            return self._read_u2()
        if t0 == "D":  # double
            import struct
            return struct.unpack(">d", self._read_exact(8))[0]
        if t0 == "F":  # float
            import struct
            return struct.unpack(">f", self._read_exact(4))[0]
        if t0 == "I":  # int
            return self._read_s4()
        if t0 == "J":  # long
            return self._read_s8()
        if t0 == "S":  # short
            return self._read_s2()
        if t0 == "Z":  # boolean
            return self._read_u1() != 0
        if t0 in ("L", "["):  # object or array
            return self._read_content_object()
        raise NotImplementedError(f"Unsupported type code: {t0}")

    # Internal object/content reader (subset of Java Serialization)
    def _read_content_object(self):
        b = self._read_u1()
        # Dispatch on TC
        if b == self.TC_NULL:
            return None
        if b == self.TC_REFERENCE:
            handle = self._read_u4()
            if handle not in self._handles:
                raise ValueError(f"Invalid reference handle: {hex(handle)}")
            return self._handles[handle]
        if b == self.TC_STRING:
            s = self._read_mutf8_short()
            self._assign_handle(s)
            return s
        if b == self.TC_LONGSTRING:
            s = self._read_mutf8_long()
            self._assign_handle(s)
            return s
        if b == self.TC_BLOCKDATA:
            ln = self._read_u1()
            data = self._read_exact(ln)
            return data
        if b == self.TC_BLOCKDATALONG:
            ln = self._read_u4()
            data = self._read_exact(ln)
            return data
        if b == self.TC_ENDBLOCKDATA:
            return _EOF  # treat end-blockdata as internal marker
        if b in (self.TC_OBJECT, self.TC_CLASSDESC, self.TC_ARRAY, self.TC_CLASS,
                 self.TC_PROXYCLASSDESC, self.TC_ENUM, self.TC_EXCEPTION, self.TC_RESET):
            # Basic skipping strategy for unsupported types: try to skip a block or raise
            # For safety, we raise to avoid infinite loops on unknown structures.
            raise NotImplementedError(
                f"Unsupported type code 0x{b:02x} in this minimal parser")
        # If it's not a known TC marker, treat it as raw byte data preceded by length?
        # Rewind one byte and try to read as plain bytes until EOF (fallback).
        self._seek_rel(-1)
        rest = self._read_exact(self._remaining())
        return rest

    # Handle table management
    def _assign_handle(self, obj):
        self._handles[self._next_handle] = obj
        self._next_handle += 1

    # Reading helpers
    def _read_exact(self, n):
        if n < 0:
            raise ValueError("Negative read")
        data = self._io.read(n)
        if data is None or len(data) != n:
            raise EOFError("Unexpected EOF")
        self._pos += n
        return data

    def _read_u1(self):
        b = self._read_exact(1)
        return b[0]

    def _read_s1(self):
        v = self._read_u1()
        return v - 256 if v > 127 else v

    def _read_u2(self):
        import struct
        return struct.unpack(">H", self._read_exact(2))[0]

    def _read_s2(self):
        import struct
        return struct.unpack(">h", self._read_exact(2))[0]

    def _read_u4(self):
        import struct
        return struct.unpack(">I", self._read_exact(4))[0]

    def _read_s4(self):
        import struct
        return struct.unpack(">i", self._read_exact(4))[0]

    def _read_s8(self):
        import struct
        return struct.unpack(">q", self._read_exact(8))[0]

    def _read_mutf8_short(self):
        ln = self._read_u2()
        data = self._read_exact(ln)
        # Best-effort decode: Java uses modified UTF-8; for ASCII and standard UTF-8 this works.
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("utf-8", errors="replace")

    def _read_mutf8_long(self):
        ln = self._read_s8()
        if ln < 0:
            raise ValueError("Negative long string length")
        data = self._read_exact(ln)
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("utf-8", errors="replace")

    def _seek_rel(self, off):
        self._io.seek(off, 1)
        self._pos += off

    def _remaining(self):
        return self._len - self._pos


class _EOFType:
    pass


_EOF = _EOFType()

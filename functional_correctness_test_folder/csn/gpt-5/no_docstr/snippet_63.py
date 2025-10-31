class StreamingFile:

    def __init__(self, data_stream):
        self._it = iter(data_stream)
        self._chunks = []
        self._total_len = 0
        self._type = None  # 'bytes' or 'str'
        self._eof = False
        self._empty = b''

    def _set_type_from_chunk(self, chunk):
        if isinstance(chunk, (bytes, bytearray)):
            self._type = 'bytes'
            self._empty = b''
        elif isinstance(chunk, str):
            self._type = 'str'
            self._empty = ''
        else:
            raise TypeError("Stream must yield bytes or str")
        # normalize bytearray to bytes
        if isinstance(chunk, bytearray):
            return bytes(chunk)
        return chunk

    def _add_chunk(self, chunk):
        if chunk is None:
            return
        if self._type is None:
            chunk = self._set_type_from_chunk(chunk)
        else:
            if self._type == 'bytes':
                if isinstance(chunk, bytearray):
                    chunk = bytes(chunk)
                if not isinstance(chunk, (bytes,)):
                    raise TypeError("Mixed stream types: expected bytes")
            else:
                if not isinstance(chunk, str):
                    raise TypeError("Mixed stream types: expected str")
        if chunk:
            self._chunks.append(chunk)
            self._total_len += len(chunk)

    def _fetch_next(self):
        if self._eof:
            return False
        try:
            chunk = next(self._it)
        except StopIteration:
            self._eof = True
            return False
        self._add_chunk(chunk)
        return True

    def _join(self, parts):
        if not parts:
            return self._empty
        if self._type == 'bytes':
            return b''.join(parts)
        else:
            return ''.join(parts)

    def read(self, size=None):
        if size is not None and not isinstance(size, int):
            raise TypeError("size must be an int or None")
        if size is not None and size < 0:
            size = None

        if size is None:
            # read all remaining
            while self._fetch_next():
                pass
            if not self._chunks:
                return self._empty
            result = self._join(self._chunks)
            self._chunks.clear()
            self._total_len = 0
            return result

        # size == 0
        if size == 0:
            return self._empty

        # ensure we have at least size bytes/chars or EOF
        while self._total_len < size and self._fetch_next():
            pass

        if not self._chunks:
            return self._empty

        remaining = size
        out_parts = []
        while remaining > 0 and self._chunks:
            first = self._chunks[0]
            flen = len(first)
            if flen <= remaining:
                out_parts.append(first)
                self._chunks.pop(0)
                remaining -= flen
                self._total_len -= flen
            else:
                # split the chunk
                out_parts.append(first[:remaining])
                self._chunks[0] = first[remaining:]
                self._total_len -= remaining
                remaining = 0

        return self._join(out_parts)

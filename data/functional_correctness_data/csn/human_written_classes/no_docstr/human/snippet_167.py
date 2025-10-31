class GzipReader:
    GZIP = 1
    DEFLATE = 2

    def __init__(self, rfile, encoding=GZIP, readChunkSize=512):
        self.rfile = rfile
        self.chunks = []
        self.bufSize = 0
        assert encoding in (GzipReader.GZIP, GzipReader.DEFLATE)
        self.encoding = encoding
        self.unzip = None
        self.readChunkSize = readChunkSize

    def _CreateUnzip(self, firstChunk):
        import zlib
        if self.encoding == GzipReader.GZIP:
            wbits = zlib.MAX_WBITS + 16
        elif self.encoding == GzipReader.DEFLATE:
            chunkLen = len(firstChunk)
            wbits = -zlib.MAX_WBITS
            if firstChunk[:3] == ['\x1f', '\x8b', '\x08']:
                wbits = zlib.MAX_WBITS + 16
            elif chunkLen >= 2:
                b0 = ord(firstChunk[0])
                b1 = ord(firstChunk[1])
                if b0 & 15 == 8 and (b0 * 256 + b1) % 31 == 0:
                    wbits = min(((b0 & 240) >> 4) + 8, zlib.MAX_WBITS)
        else:
            assert False
        self.unzip = zlib.decompressobj(wbits)
        return self.unzip

    def read(self, bytes=-1):
        chunks = self.chunks
        bufSize = self.bufSize
        while bufSize < bytes or bytes == -1:
            chunk = self.rfile.read(self.readChunkSize)
            if self.unzip is None:
                self._CreateUnzip(chunk)
            if chunk:
                inflatedChunk = self.unzip.decompress(chunk)
                bufSize += len(inflatedChunk)
                chunks.append(inflatedChunk)
            else:
                break
        if bufSize <= bytes or bytes == -1:
            leftoverBytes = 0
            leftoverChunks = []
        else:
            leftoverBytes = bufSize - bytes
            lastChunk = chunks.pop()
            chunks.append(lastChunk[:-leftoverBytes])
            leftoverChunks = [lastChunk[-leftoverBytes:]]
        self.chunks = leftoverChunks
        self.bufSize = leftoverBytes
        buf = b''.join(chunks)
        return buf
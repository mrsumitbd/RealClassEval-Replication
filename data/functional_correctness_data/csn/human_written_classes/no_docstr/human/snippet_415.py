class _BufferedWriter:
    _sslSocket = None
    _internalBuffer = None
    _writingInProgress = False
    _requestedDataLength = -1

    def __init__(self, sslSocket):
        self._sslSocket = sslSocket
        self._internalBuffer = bytearray()
        self._writingInProgress = False
        self._requestedDataLength = -1

    def _reset(self):
        self._internalBuffer = bytearray()
        self._writingInProgress = False
        self._requestedDataLength = -1

    def write(self, encodedData, payloadLength):
        if not self._writingInProgress:
            self._internalBuffer = encodedData
            self._writingInProgress = True
            self._requestedDataLength = payloadLength
        lengthWritten = self._sslSocket.write(self._internalBuffer)
        self._internalBuffer = self._internalBuffer[lengthWritten:]
        if len(self._internalBuffer) == 0:
            ret = self._requestedDataLength
            self._reset()
            return ret
        else:
            return 0
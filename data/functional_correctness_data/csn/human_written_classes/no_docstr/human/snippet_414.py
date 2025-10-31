import errno
import socket

class _BufferedReader:
    _sslSocket = None
    _internalBuffer = None
    _remainedLength = -1
    _bufferingInProgress = False

    def __init__(self, sslSocket):
        self._sslSocket = sslSocket
        self._internalBuffer = bytearray()
        self._bufferingInProgress = False

    def _reset(self):
        self._internalBuffer = bytearray()
        self._remainedLength = -1
        self._bufferingInProgress = False

    def read(self, numberOfBytesToBeBuffered):
        if not self._bufferingInProgress:
            self._remainedLength = numberOfBytesToBeBuffered
            self._bufferingInProgress = True
        while self._remainedLength > 0:
            dataChunk = self._sslSocket.read(self._remainedLength)
            if not dataChunk:
                raise socket.error(errno.ECONNABORTED, 0)
            self._internalBuffer.extend(dataChunk)
            self._remainedLength -= len(dataChunk)
        ret = self._internalBuffer
        self._reset()
        return ret
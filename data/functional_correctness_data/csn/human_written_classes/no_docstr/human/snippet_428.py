class QR8bitByte:

    def __init__(self, data):
        self.mode = QRMode.MODE_8BIT_BYTE
        self.data = data

    def getLength(self):
        return len(self.data)

    def write(self, buffer):
        for i in range(len(self.data)):
            buffer.put(ord(self.data[i]), 8)

    def __repr__(self):
        return self.data
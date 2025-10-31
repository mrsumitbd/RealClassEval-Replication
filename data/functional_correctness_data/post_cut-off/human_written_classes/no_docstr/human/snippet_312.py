class FakeSerial:

    def __init__(self):
        self.data = b''

    def write(self, data):
        print('发送数据: ', end='')
        for i in data:
            print(f'{i:02x}', end=' ')
        print()

    def setRTS(self, b):
        pass

    def read(self, n):
        return b'\x01\x03\x02\x00\x19y\x8e'

    def close(self):
        pass
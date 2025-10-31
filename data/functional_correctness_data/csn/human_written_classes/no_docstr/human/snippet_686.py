class MultiframeDiagnosticMessage:

    def __init__(self, response):
        self.id = response['id']
        self.mode = response['mode']
        self.bus = response['bus']
        self.pid = response['pid']
        self.payload = '0x' + response['payload'][8:]

    def addFrame(self, response):
        self.payload += response['payload'][2:]

    def getResponse(self):
        request = {'timestamp': 0, 'bus': self.bus, 'id': self.id, 'mode': self.mode, 'success': True, 'pid': self.pid, 'payload': self.payload}
        return request
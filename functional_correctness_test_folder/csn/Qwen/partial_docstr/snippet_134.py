
class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast

    def _handle_request(self):
        '''Request handler for SlaveSerialWorker'''
        request = self.serial_w.read_request()
        if request:
            response = self.mbus_cli.execute(request, slave=self.slave_addr)
            self.serial_w.send_response(response)

    def run(self):
        while True:
            self._handle_request()

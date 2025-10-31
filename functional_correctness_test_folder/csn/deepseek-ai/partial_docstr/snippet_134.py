
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
            if self.allow_bcast or request.slave_id == self.slave_addr:
                response = self.mbus_cli.execute(request)
                self.serial_w.write_response(response)

    def run(self):
        while True:
            self._handle_request()

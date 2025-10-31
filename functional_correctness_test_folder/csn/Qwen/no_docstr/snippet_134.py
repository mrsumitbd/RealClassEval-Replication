
class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast

    def _handle_request(self):
        request = self.serial_w.read()
        if request:
            response = self.mbus_cli.execute(self.slave_addr, request)
            self.serial_w.write(response)

    def run(self):
        while True:
            self._handle_request()

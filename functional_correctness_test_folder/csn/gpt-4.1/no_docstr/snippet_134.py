
class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast

    def _handle_request(self):
        # Read request from serial
        req = self.serial_w.read()
        if not req:
            return
        # Check address
        addr = req[0]
        if addr == self.slave_addr or (self.allow_bcast and addr == 0):
            # Forward to Modbus client
            resp = self.mbus_cli.execute(req)
            if resp is not None and addr != 0:  # Don't respond to broadcast
                self.serial_w.write(resp)

    def run(self):
        while True:
            self._handle_request()

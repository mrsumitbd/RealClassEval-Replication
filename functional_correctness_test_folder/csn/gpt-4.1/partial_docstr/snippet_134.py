
class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast
        self._running = False

    def _handle_request(self):
        '''Request handler for SlaveSerialWorker'''
        # Read request from serial
        req = self.serial_w.read_request()
        if req is None:
            return
        # Check address
        addr = req.get('address', None)
        if addr is None:
            return
        if addr != self.slave_addr and (not self.allow_bcast or addr != 0):
            # Not for us
            return
        # Forward to Modbus client
        try:
            response = self.mbus_cli.execute(req)
        except Exception as e:
            response = {'error': str(e)}
        # Write response to serial
        self.serial_w.write_response(response)

    def run(self):
        self._running = True
        while self._running:
            self._handle_request()

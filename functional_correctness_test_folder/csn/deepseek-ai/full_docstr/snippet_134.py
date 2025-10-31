
class Serial2ModbusClient:
    ''' Customize a slave serial worker for map a modbus TCP client. '''

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        '''Serial2ModbusClient constructor.
        :param serial_w: a SlaveSerialWorker instance
        :type serial_w: SlaveSerialWorker
        :param mbus_cli: a ModbusClient instance
        :type mbus_cli: ModbusClient
        :param slave_addr: modbus slave address
        :type slave_addr: int
        :param allow_bcast: allow processing broadcast frames (slave @0)
        :type allow_bcast: bool
        '''
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast
        self.serial_w.set_request_handler(self._handle_request)

    def _handle_request(self, request):
        '''Request handler for SlaveSerialWorker'''
        if not request:
            return None

        if request[0] == 0 and not self.allow_bcast:
            return None

        if request[0] != self.slave_addr and request[0] != 0:
            return None

        try:
            response = self.mbus_cli.execute(request)
            return response
        except Exception:
            return None

    def run(self):
        '''Start serial processing.'''
        self.serial_w.start()

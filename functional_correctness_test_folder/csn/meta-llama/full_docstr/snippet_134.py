
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
        if (request.slave_id == self.slave_addr) or (request.slave_id == 0 and self.allow_bcast):
            response = self.mbus_cli.execute(request)
            if response is not None:
                self.serial_w.send_response(response)

    def run(self):
        '''Start serial processing.'''
        self.serial_w.run()

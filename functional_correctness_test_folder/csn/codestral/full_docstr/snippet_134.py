
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

    def _handle_request(self):
        '''Request handler for SlaveSerialWorker'''
        request = self.serial_w.get_request()
        if request:
            if self.allow_bcast or request.slave_addr == self.slave_addr:
                response = self.mbus_cli.execute(
                    request.function_code, request.data)
                self.serial_w.send_response(response)

    def run(self):
        '''Start serial processing.'''
        while True:
            self._handle_request()

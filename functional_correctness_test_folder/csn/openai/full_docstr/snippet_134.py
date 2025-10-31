
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

        # Register the request handler with the serial worker.
        # The worker is expected to call this method with a ModbusRequest instance.
        try:
            # Preferred API
            self.serial_w.register_request_handler(self._handle_request)
        except AttributeError:
            # Fallback API
            try:
                self.serial_w.set_request_handler(self._handle_request)
            except AttributeError:
                # If the worker does not support callbacks, we cannot proceed.
                raise RuntimeError(
                    "The provided serial worker does not expose a request handler registration method."
                )

    def _handle_request(self, request):
        '''Request


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
        req = self.serial_w.read_request()
        if req is None or len(req) < 2:
            return

        addr = req[0]
        if addr != self.slave_addr and (not (self.allow_bcast and addr == 0)):
            # Not for us, ignore
            return

        # Remove address and CRC (last 2 bytes)
        pdu = req[1:-2]
        try:
            resp_pdu = self.mbus_cli.execute_pdu(pdu)
        except Exception:
            # On error, do not respond
            return

        if addr == 0:
            # Broadcast, do not send response
            return

        # Build response: address + response PDU + CRC
        resp = bytes([addr]) + resp_pdu
        crc = self._modbus_crc(resp)
        resp += crc.to_bytes(2, 'little')
        self.serial_w.write_response(resp)

    def run(self):
        '''Start serial processing.'''
        while True:
            self._handle_request()

    @staticmethod
    def _modbus_crc(data):
        crc = 0xFFFF
        for b in data:
            crc ^= b
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc

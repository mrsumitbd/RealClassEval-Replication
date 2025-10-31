class SlaveSerialWorker:
    """ A serial worker to manage I/O with RTU master device. """

    def __init__(self, port, end_of_frame=0.05):
        self.serial_port = port
        self.end_of_frame = end_of_frame
        self.request = ModbusRTUFrame()
        self.response = ModbusRTUFrame()

    def handle_request(self):
        """Default PDU request processing here, you must implement it in your app."""
        raise RuntimeError('implement this')

    def run(self):
        """Serial worker process."""
        self.serial_port.reset_input_buffer()
        while True:
            self.request = ModbusRTUFrame()
            self.response = ModbusRTUFrame()
            self.serial_port.timeout = None
            rx_raw = self.serial_port.read(1)
            if rx_raw:
                self.serial_port.timeout = self.end_of_frame
                while True:
                    rx_chunk = self.serial_port.read(256)
                    if not rx_chunk:
                        break
                    else:
                        rx_raw += rx_chunk
            self.request.raw = rx_raw
            crc_ok = self.request.is_valid
            logger.debug('Receive: %s (CRC %s)' % (self.request, 'OK' if crc_ok else 'ERROR'))
            if not crc_ok:
                continue
            self.handle_request()
            if self.response.is_set:
                logger.debug('Send: %s' % self.response)
                self.serial_port.write(self.response.raw)
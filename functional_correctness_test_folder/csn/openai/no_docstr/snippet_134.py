
class Serial2ModbusClient:
    """
    A simple bridge that reads Modbus requests from a serial-like object,
    forwards them to a Modbus client, and writes back the response.
    """

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        """
        Parameters
        ----------
        serial_w : file-like object
            An object that supports `readline()` and `write()` for serial communication.
        mbus_cli : object
            An object that implements a `send_request(bytes) -> bytes` method.
        slave_addr : int, optional
            The Modbus slave address this bridge should accept. Default is 1.
        allow_bcast : bool, optional
            If True, broadcast requests (address 0) are forwarded to the Modbus client.
            Default is False.
        """
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast
        self._running = False

    def _handle_request(self):
        """
        Read a single Modbus request from the serial interface, forward it to the
        Modbus client, and write the response back to the serial interface.
        """
        # Read a line from the serial interface
        raw = self.serial_w.readline()
        if not raw:
            return

        # Strip whitespace and convert to bytes
        line = raw.strip()
        if not line:
            return

        try:
            # Accept both bytes and str input
            if isinstance(line, bytes):
                line = line.decode(errors="ignore")
            req_bytes = bytes.fromhex(line)
        except Exception:
            # Invalid hex string; ignore
            return

        if not req_bytes:
            return

        # Check slave address
        addr = req_bytes[0]
        if addr != self.slave_addr and not (self.allow_bcast and addr == 0):
            return

        # Forward request to Modbus client
        try:
            resp = self.mbus_cli.send_request(req_bytes)
        except Exception:
            resp = None

        if resp is None:
            return

        # For broadcast requests, no response is expected unless allowed
        if addr == 0 and not self.allow_bcast:
            return

        # Write response back to serial interface
        try:
            hex_resp = resp.hex().upper()
            self.serial_w.write((hex_resp + "\n").encode())
        except Exception:
            # Ignore write errors
            pass

    def run(self):
        """
        Continuously read from the serial interface and process requests.
        """
        self._running = True
        while self._running:
            try:
                self._handle_request()
            except Exception:
                # Silently ignore any unexpected errors to keep the loop running
                pass

    def stop(self):
        """
        Stop the run loop.
        """
        self._running = False

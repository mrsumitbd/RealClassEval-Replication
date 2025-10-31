
import time
import threading


class Serial2ModbusClient:
    """
    A simple bridge that forwards Modbus RTU frames received on a serial
    interface to a Modbus client and writes back the response.
    """

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        """
        Parameters
        ----------
        serial_w : object
            An object that provides `read()` and `write(data)` methods.
            `read()` should return a bytes object containing a complete
            Modbus RTU frame or an empty bytes object if nothing is
            available.
        mbus_cli : object
            An object that provides a `send(request)` method which
            accepts a Modbus RTU frame (bytes) and returns the
            corresponding response frame (bytes).
        slave_addr : int, optional
            The Modbus slave address that this bridge will respond to.
            Default is 1.
        allow_bcast : bool, optional
            If True, broadcast frames (address 0) will be forwarded to
            the Modbus client. Default is False.
        """
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr & 0xFF
        self.allow_bcast = bool(allow_bcast)
        self._running = False
        self._thread = None

    def _handle_request(self):
        """
        Read a request from the serial worker, forward it to the Modbus
        client if the address matches, and write back the response.
        """
        try:
            request = self.serial_w.read()
        except Exception:
            # If read fails, ignore and continue
            return

        if not request:
            return

        # Basic sanity check: at least address + function + CRC
        if len(request) < 4:
            return

        addr = request[0]
        # Check if this frame is for us or a broadcast (if allowed)
        if addr != self.slave_addr and not (self.allow_bcast and addr == 0x00):
            return

        try:
            response = self.mbus_cli.send(request)
        except Exception:
            # If the client fails, we do not send a response
            return

        if response:
            try:
                self.serial_w.write(response)
            except Exception:
                # Ignore write errors
                pass

    def run(self):
        """
        Start the bridge loop in a separate thread. The loop will keep
        running until `stop()` is called.
        """
        if self._running:
            return  # Already running

        self._running = True

        def _loop():
            while self._running:
                self._handle_request()
                # Small sleep to avoid busy waiting if no data
                time.sleep(0.01)

        self._thread = threading.Thread(target=_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """
        Stop the bridge loop and wait for the thread to finish.
        """
        self._running = False
        if self._thread:
            self._thread.join()
            self._thread = None

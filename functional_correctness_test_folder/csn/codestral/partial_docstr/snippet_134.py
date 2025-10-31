
import threading


class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):

        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast
        self._stop_event = threading.Event()

    def _handle_request(self):
        '''Request handler for SlaveSerialWorker'''
        while not self._stop_event.is_set():
            request = self.serial_w.read_request()
            if request:
                response = self.mbus_cli.handle_request(
                    request, self.slave_addr, self.allow_bcast)
                if response:
                    self.serial_w.write_response(response)

    def run(self):

        self._stop_event.clear()
        handler_thread = threading.Thread(target=self._handle_request)
        handler_thread.start()

        try:
            while not self._stop_event.is_set():
                pass
        except KeyboardInterrupt:
            self._stop_event.set()
            handler_thread.join()

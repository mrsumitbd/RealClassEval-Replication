
import threading
import time


class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast
        self.serial_w.set_request_handler(self._handle_request)

    def _handle_request(self, request):
        '''Request handler for SlaveSerialWorker'''
        try:
            response = self.mbus_cli.send_request(
                request, self.slave_addr, self.allow_bcast)
            if response is not None:
                self.serial_w.send_response(response)
        except Exception as e:
            print(f"Error handling request: {e}")

    def run(self):
        self.serial_w.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.serial_w.stop()


import serial
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.exceptions import ModbusIOException
from pymodbus.pdu import ExceptionResponse


class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        self.serial_w = serial.Serial(**serial_w)
        self.mbus_cli = ModbusClient(**mbus_cli, framer=ModbusRtuFramer)
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast
        self.mbus_cli.connect()

    def _handle_request(self):
        request = self.serial_w.read(256)
        if len(request) > 0:
            try:
                response = self.mbus_cli.execute(request, unit=self.slave_addr)
                if isinstance(response, ModbusIOException) or isinstance(response, ExceptionResponse):
                    # Handle Modbus exception or IO exception
                    # or some other error indicator
                    self.serial_w.write(b'\x00')
                else:
                    self.serial_w.write(response.encode())
            except Exception as e:
                # Handle other exceptions
                self.serial_w.write(b'\x00')  # or some other error indicator

    def run(self):
        while True:
            self._handle_request()

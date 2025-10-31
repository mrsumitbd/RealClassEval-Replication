
import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu


class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):

        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast

    def _handle_request(self):

        request = self.serial_w.readline().decode('utf-8').strip()
        if request:
            try:
                if request.startswith('read_coils'):
                    _, start_addr, count = request.split()
                    start_addr, count = int(start_addr), int(count)
                    response = self.mbus_cli.execute(
                        self.slave_addr, cst.READ_COILS, start_addr, count)
                    self.serial_w.write(
                        f"read_coils_response {response}\n".encode('utf-8'))
                elif request.startswith('read_holding_registers'):
                    _, start_addr, count = request.split()
                    start_addr, count = int(start_addr), int(count)
                    response = self.mbus_cli.execute(
                        self.slave_addr, cst.READ_HOLDING_REGISTERS, start_addr, count)
                    self.serial_w.write(
                        f"read_holding_registers_response {response}\n".encode('utf-8'))
                elif request.startswith('write_single_coil'):
                    _, coil_addr, value = request.split()
                    coil_addr, value = int(coil_addr), int(value)
                    response = self.mbus_cli.execute(
                        self.slave_addr, cst.WRITE_SINGLE_COIL, coil_addr, output_value=value)
                    self.serial_w.write(
                        f"write_single_coil_response {response}\n".encode('utf-8'))
                elif request.startswith('write_single_register'):
                    _, reg_addr, value = request.split()
                    reg_addr, value = int(reg_addr), int(value)
                    response = self.mbus_cli.execute(
                        self.slave_addr, cst.WRITE_SINGLE_REGISTER, reg_addr, output_value=value)
                    self.serial_w.write(
                        f"write_single_register_response {response}\n".encode('utf-8'))
                elif request.startswith('broadcast'):
                    if self.allow_bcast:
                        _, function_code, *data = request.split()
                        function_code = int(function_code)
                        data = [int(d) for d in data]
                        self.mbus_cli.execute(0, function_code, *data)
                        self.serial_w.write(
                            "broadcast_response OK\n".encode('utf-8'))
                    else:
                        self.serial_w.write(
                            "broadcast_response Not allowed\n".encode('utf-8'))
            except Exception as e:
                self.serial_w.write(f"error {str(e)}\n".encode('utf-8'))

    def run(self):

        while True:
            self._handle_request()

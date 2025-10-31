
import serial
import minimalmodbus


class Serial2ModbusClient:

    def __init__(self, serial_w, mbus_cli, slave_addr=1, allow_bcast=False):
        self.serial_w = serial_w
        self.mbus_cli = mbus_cli
        self.slave_addr = slave_addr
        self.allow_bcast = allow_bcast

    def _handle_request(self):
        try:
            request = self.serial_w.readline().strip()
            if not request:
                return None

            parts = request.split()
            if len(parts) < 2:
                return None

            function_code = int(parts[0])
            register_address = int(parts[1])

            if function_code == 3:  # Read holding registers
                if len(parts) < 3:
                    return None
                count = int(parts[2])
                data = self.mbus_cli.read_registers(register_address, count)
                return f"{function_code} {register_address} {count} {' '.join(map(str, data))}"

            elif function_code == 6:  # Write single register
                if len(parts) < 3:
                    return None
                value = int(parts[2])
                self.mbus_cli.write_register(register_address, value)
                return f"{function_code} {register_address} {value}"

            elif function_code == 16:  # Write multiple registers
                if len(parts) < 4:
                    return None
                count = int(parts[2])
                values = list(map(int, parts[3:3+count]))
                self.mbus_cli.write_registers(register_address, values)
                return f"{function_code} {register_address} {count} {' '.join(map(str, values))}"

            else:
                return None

        except Exception as e:
            print(f"Error handling request: {e}")
            return None

    def run(self):
        while True:
            try:
                response = self._handle_request()
                if response is not None:
                    self.serial_w.write(response.encode() + b'\n')
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in run loop: {e}")

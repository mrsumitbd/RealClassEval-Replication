import serial
import threading
import json
import threading
import struct

class TempSensorNode:

    def __init__(self, port, warning, address, baudrate=9600):
        self._value = 0.0
        self.warning = warning
        self.device_id = address
        self.success = False
        self.hardware_interface = serial.Serial(port=port, baudrate=baudrate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
        self.lock = threading.Lock()

    def calculate_crc(self, data):
        crc = 65535
        for pos in data:
            crc ^= pos
            for i in range(8):
                if crc & 1 != 0:
                    crc >>= 1
                    crc ^= 40961
                else:
                    crc >>= 1
        return crc

    def build_modbus_request(self, device_id, function_code, register_address, register_count):
        request = struct.pack('>BBHH', device_id, function_code, register_address, register_count)
        crc = self.calculate_crc(request)
        request += struct.pack('<H', crc)
        return request

    def read_modbus_response(self, response):
        if len(response) < 5:
            return None
        data = response[:-2]
        crc_received = struct.unpack('<H', response[-2:])[0]
        crc_calculated = self.calculate_crc(data)
        if crc_received == crc_calculated:
            return data[3:]
        return None

    def send_prototype_command(self, command):
        function_code = 4
        register_address = 3
        register_count = 2
        request = self.build_modbus_request(command, function_code, register_address, register_count)
        self.hardware_interface.write(request)
        response = self.hardware_interface.read(9)
        data = self.read_modbus_response(response)
        if data is None:
            return None
        high_value = struct.unpack('>H', data[:2])[0]
        low_value = struct.unpack('>H', data[2:])[0]
        raw_temperature = high_value << 16 | low_value
        if raw_temperature & 32768:
            raw_temperature -= 65536
        actual_temperature = raw_temperature / 10.0
        return actual_temperature

    @property
    def value(self) -> float:
        self._value = self.send_prototype_command(self.device_id)
        return self._value

    def set_warning(self, command):
        self.success = False
        temp = json.loads(command)['warning_temp']
        self.warning = round(float(temp), 1)
        self.success = True
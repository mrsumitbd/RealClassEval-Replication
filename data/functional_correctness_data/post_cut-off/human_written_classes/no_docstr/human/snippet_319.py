import struct
import serial

class TempSensor:

    def __init__(self, port, baudrate=9600):
        self.ser = serial.Serial(port=port, baudrate=baudrate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)

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

    def send_command(self, command):
        function_code = 4
        register_address = 3
        register_count = 2
        request = self.build_modbus_request(command, function_code, register_address, register_count)
        self.ser.write(request)
        response = self.ser.read(9)
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
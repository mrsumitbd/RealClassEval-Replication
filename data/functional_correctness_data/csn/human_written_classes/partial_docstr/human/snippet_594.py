from datetime import datetime, timedelta

class HistoryEntry:
    """Entry in the history of the device."""

    def __init__(self, byte_array):
        self.device_time = None
        self.wall_time = None
        self.temperature = None
        self.light = None
        self.moisture = None
        self.conductivity = None
        self._decode_history(byte_array)

    def _decode_history(self, byte_array):
        """Perform byte magic when decoding history data."""
        temp_bytes = byte_array[4:6]
        if temp_bytes[1] & 128 > 0:
            temp_bytes = [temp_bytes[0] ^ 255, temp_bytes[1] ^ 255]
        self.device_time = int.from_bytes(byte_array[:4], BYTEORDER)
        self.temperature = int.from_bytes(temp_bytes, BYTEORDER) / 10.0
        self.light = int.from_bytes(byte_array[7:10], BYTEORDER)
        self.moisture = byte_array[11]
        self.conductivity = int.from_bytes(byte_array[12:14], BYTEORDER)
        _LOGGER.debug('Raw data for char 0x3c: %s', format_bytes(byte_array))
        _LOGGER.debug('device time: %d', self.device_time)
        _LOGGER.debug('temp: %f', self.temperature)
        _LOGGER.debug('brightness: %d', self.light)
        _LOGGER.debug('conductivity: %d', self.conductivity)
        _LOGGER.debug('moisture: %d', self.moisture)

    def compute_wall_time(self, time_diff):
        """Correct the device time to the wall time. """
        self.wall_time = datetime.fromtimestamp(self.device_time + time_diff)
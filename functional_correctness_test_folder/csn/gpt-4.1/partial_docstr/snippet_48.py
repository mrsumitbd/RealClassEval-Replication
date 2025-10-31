
import datetime as dt


class Datetime:

    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        # Broadlink protocol: [year, month, day, hour, minute, second, weekday, 0]
        # year: 2 bytes, little endian
        year = datetime.year
        packed = bytearray(8)
        packed[0] = year & 0xFF
        packed[1] = (year >> 8) & 0xFF
        packed[2] = datetime.minute
        packed[3] = datetime.hour
        packed[4] = datetime.day
        packed[5] = datetime.month
        # Broadlink: 0=Sunday, 1=Monday, ..., 6=Saturday
        packed[6] = datetime.isoweekday() % 7
        packed[7] = 0
        return bytes(packed)

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        '''Unpack a timestamp received over the Broadlink protocol.'''
        if len(data) < 8:
            raise ValueError("Data must be at least 8 bytes")
        year = data[0] | (data[1] << 8)
        minute = data[2]
        hour = data[3]
        day = data[4]
        month = data[5]
        # data[6] is weekday, data[7] is reserved
        return dt.datetime(year, month, day, hour, minute, 0)

    @staticmethod
    def now() -> dt.datetime:
        return dt.datetime.now()

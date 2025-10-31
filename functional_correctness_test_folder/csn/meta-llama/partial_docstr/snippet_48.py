
import datetime as dt


class Datetime:

    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        """Pack a datetime object into bytes according to the Broadlink protocol."""
        year = datetime.year - 1900
        month = datetime.month
        day = datetime.day
        hour = datetime.hour
        minute = datetime.minute
        second = datetime.second
        return bytes([year & 0xFF, (year >> 8) & 0xFF, month, day, hour, minute, second])

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        '''Unpack a timestamp received over the Broadlink protocol.'''
        year = data[0] + (data[1] << 8) + 1900
        month = data[2]
        day = data[3]
        hour = data[4]
        minute = data[5]
        second = data[6]
        return dt.datetime(year, month, day, hour, minute, second)

    @staticmethod
    def now() -> dt.datetime:
        """Return the current local date and time."""
        return dt.datetime.now()

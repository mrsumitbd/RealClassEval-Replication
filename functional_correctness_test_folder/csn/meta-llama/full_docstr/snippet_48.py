
import datetime as dt


class Datetime:
    '''Helps to pack and unpack datetime objects for the Broadlink protocol.'''
    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        '''Pack the timestamp to be sent over the Broadlink protocol.'''
        year = datetime.year
        month = datetime.month
        day = datetime.day
        hour = datetime.hour
        minute = datetime.minute
        second = datetime.second
        return bytes([
            (year >> 8) & 0xFF, year & 0xFF,
            month,
            day,
            hour,
            minute,
            second,
            datetime.isoweekday()  # Monday is 1 and Sunday is 7
        ])

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        '''Unpack a timestamp received over the Broadlink protocol.'''
        year = (data[0] << 8) + data[1]
        month = data[2]
        day = data[3]
        hour = data[4]
        minute = data[5]
        second = data[6]
        return dt.datetime(year, month, day, hour, minute, second)

    @staticmethod
    def now() -> dt.datetime:
        '''Return the current date and time with timezone info.'''
        return dt.datetime.now(dt.timezone.utc)

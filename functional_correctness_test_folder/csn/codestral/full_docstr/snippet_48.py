
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
        weekday = datetime.weekday() + 1
        year_day = datetime.timetuple().tm_yday
        is_dst = 1 if datetime.dst() else 0

        return bytes([minute, hour, day, month, year % 100, year // 100, weekday, year_day % 256, year_day // 256, is_dst, 0, 0, 0, second])

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        '''Unpack a timestamp received over the Broadlink protocol.'''
        minute, hour, day, month, year_low, year_high, weekday, year_day_low, year_day_high, is_dst, _, _, _, second = data
        year = year_low + year_high * 100
        year_day = year_day_low + year_day_high * 256

        return dt.datetime(year, month, day, hour, minute, second)

    @staticmethod
    def now() -> dt.datetime:
        '''Return the current date and time with timezone info.'''
        return dt.datetime.now(dt.timezone.utc)

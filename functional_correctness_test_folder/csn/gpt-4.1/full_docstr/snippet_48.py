
import datetime as dt


class Datetime:
    '''Helps to pack and unpack datetime objects for the Broadlink protocol.'''
    @staticmethod
    def pack(datetime_obj: dt.datetime) -> bytes:
        '''Pack the timestamp to be sent over the Broadlink protocol.'''
        if datetime_obj.tzinfo is None:
            datetime_obj = datetime_obj.replace(tzinfo=dt.timezone.utc)
        datetime_obj = datetime_obj.astimezone(dt.timezone.utc)
        year = datetime_obj.year % 100  # 2-digit year
        packed = bytes([
            year,
            datetime_obj.minute,
            datetime_obj.hour,
            datetime_obj.day,
            datetime_obj.month,
            datetime_obj.weekday(),
            0  # reserved byte, always 0
        ])
        return packed

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        '''Unpack a timestamp received over the Broadlink protocol.'''
        if len(data) < 7:
            raise ValueError("Data must be at least 7 bytes long")
        year = data[0] + 2000
        minute = data[1]
        hour = data[2]
        day = data[3]
        month = data[4]
        # data[5] is weekday, data[6] is reserved
        return dt.datetime(year, month, day, hour, minute, 0, tzinfo=dt.timezone.utc)

    @staticmethod
    def now() -> dt.datetime:
        '''Return the current date and time with timezone info.'''
        return dt.datetime.now(dt.timezone.utc)

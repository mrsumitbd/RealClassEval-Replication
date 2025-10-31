import datetime as dt
import struct


class Datetime:
    '''Helps to pack and unpack datetime objects for the Broadlink protocol.'''

    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        '''Pack the timestamp to be sent over the Broadlink protocol.'''
        if datetime.tzinfo is None:
            datetime = datetime.astimezone()
        else:
            datetime = datetime.astimezone(datetime.tzinfo)
        datetime = datetime.replace(microsecond=0)

        tz_offset_minutes = int(datetime.utcoffset().total_seconds() // 60)

        return struct.pack(
            "<HBBBBBBh",
            datetime.year,
            datetime.month,
            datetime.day,
            datetime.hour,
            datetime.minute,
            datetime.second,
            datetime.isoweekday() % 7,  # 0=Sunday, 1=Monday, ... 6=Saturday
            tz_offset_minutes,
        )

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        '''Unpack a timestamp received over the Broadlink protocol.'''
        year, month, day, hour, minute, second, weekday, tz_offset_minutes = struct.unpack(
            "<HBBBBBBh", data
        )
        tz = dt.timezone(dt.timedelta(minutes=tz_offset_minutes))
        return dt.datetime(year, month, day, hour, minute, second, tzinfo=tz)

    @staticmethod
    def now() -> dt.datetime:
        '''Return the current date and time with timezone info.'''
        return dt.datetime.now(dt.datetime.now().astimezone().tzinfo).replace(microsecond=0)


import datetime as dt


class Datetime:
    '''Helps to pack and unpack datetime objects for the Broadlink protocol.'''
    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        '''Pack the timestamp to be sent over the Broadlink protocol.'''
        year = datetime.year.to_bytes(2, 'little')
        month = datetime.month.to_bytes(1, 'little')
        day = datetime.day.to_bytes(1, 'little')
        hour = datetime.hour.to_bytes(1, 'little')
        minute = datetime.minute.to_bytes(1, 'little')
        second = datetime.second.to_bytes(1, 'little')
        microsecond = datetime.microsecond.to_bytes(4, 'little')
        weekday = datetime.weekday().to_bytes(
            1, 'little') if datetime.weekday() != 6 else (0).to_bytes(1, 'little')
        return year + month + day + hour + minute + second + microsecond + weekday

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        '''Unpack a timestamp received over the Broadlink protocol.'''
        year = int.from_bytes(data[0:2], 'little')
        month = data[2]
        day = data[3]
        hour = data[4]
        minute = data[5]
        second = data[6]
        microsecond = int.from_bytes(data[7:11], 'little')
        return dt.datetime(year, month, day, hour, minute, second, microsecond)

    @staticmethod
    def now() -> dt.datetime:
        '''Return the current date and time with timezone info.'''
        return dt.datetime.now(dt.timezone.utc).astimezone()

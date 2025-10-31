
import datetime as dt


class Datetime:

    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        year = datetime.year.to_bytes(2, byteorder='little')
        month = datetime.month.to_bytes(1, byteorder='little')
        day = datetime.day.to_bytes(1, byteorder='little')
        hour = datetime.hour.to_bytes(1, byteorder='little')
        minute = datetime.minute.to_bytes(1, byteorder='little')
        second = datetime.second.to_bytes(1, byteorder='little')
        microsecond = datetime.microsecond.to_bytes(4, byteorder='little')
        weekday = datetime.weekday().to_bytes(1, byteorder='little')
        return year + month + day + hour + minute + second + microsecond + weekday

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        '''Unpack a timestamp received over the Broadlink protocol.'''
        year = int.from_bytes(data[0:2], byteorder='little')
        month = data[2]
        day = data[3]
        hour = data[4]
        minute = data[5]
        second = data[6]
        microsecond = int.from_bytes(data[7:11], byteorder='little')
        return dt.datetime(year, month, day, hour, minute, second, microsecond)

    @staticmethod
    def now() -> dt.datetime:
        return dt.datetime.now()

import time
import datetime as dt

class Datetime:
    """Helps to pack and unpack datetime objects for the Broadlink protocol."""

    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        """Pack the timestamp to be sent over the Broadlink protocol."""
        data = bytearray(12)
        utcoffset = int(datetime.utcoffset().total_seconds() / 3600)
        data[:4] = utcoffset.to_bytes(4, 'little', signed=True)
        data[4:6] = datetime.year.to_bytes(2, 'little')
        data[6] = datetime.minute
        data[7] = datetime.hour
        data[8] = int(datetime.strftime('%y'))
        data[9] = datetime.isoweekday()
        data[10] = datetime.day
        data[11] = datetime.month
        return data

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        """Unpack a timestamp received over the Broadlink protocol."""
        utcoffset = int.from_bytes(data[0:4], 'little', signed=True)
        year = int.from_bytes(data[4:6], 'little')
        minute = data[6]
        hour = data[7]
        subyear = data[8]
        isoweekday = data[9]
        day = data[10]
        month = data[11]
        tz_info = dt.timezone(dt.timedelta(hours=utcoffset))
        datetime = dt.datetime(year, month, day, hour, minute, 0, 0, tz_info)
        if datetime.isoweekday() != isoweekday:
            raise ValueError('isoweekday does not match')
        if int(datetime.strftime('%y')) != subyear:
            raise ValueError('subyear does not match')
        return datetime

    @staticmethod
    def now() -> dt.datetime:
        """Return the current date and time with timezone info."""
        tz_info = dt.timezone(dt.timedelta(seconds=-time.timezone))
        return dt.datetime.now(tz_info)
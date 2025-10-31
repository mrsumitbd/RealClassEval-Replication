
import datetime as dt
import struct


class Datetime:

    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        """Packs a datetime object into bytes."""
        timestamp = int(datetime.timestamp())
        return struct.pack('!q', timestamp)

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        """Unpacks bytes into a datetime object."""
        timestamp = struct.unpack('!q', data)[0]
        return dt.datetime.fromtimestamp(timestamp)

    @staticmethod
    def now() -> dt.datetime:
        """Returns the current datetime."""
        return dt.datetime.now()

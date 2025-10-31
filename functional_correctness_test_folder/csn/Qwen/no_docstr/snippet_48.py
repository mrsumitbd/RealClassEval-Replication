
import datetime as dt
import struct


class Datetime:

    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        timestamp = datetime.timestamp()
        return struct.pack('!d', timestamp)

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        timestamp = struct.unpack('!d', data)[0]
        return dt.datetime.fromtimestamp(timestamp)

    @staticmethod
    def now() -> dt.datetime:
        return dt.datetime.now()

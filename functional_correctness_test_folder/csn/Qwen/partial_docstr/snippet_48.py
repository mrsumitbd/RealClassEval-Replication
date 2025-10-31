
import datetime as dt
import struct


class Datetime:

    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        timestamp = int(datetime.timestamp())
        return struct.pack('>I', timestamp)

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        timestamp = struct.unpack('>I', data)[0]
        return dt.datetime.fromtimestamp(timestamp)

    @staticmethod
    def now() -> dt.datetime:
        return dt.datetime.now()

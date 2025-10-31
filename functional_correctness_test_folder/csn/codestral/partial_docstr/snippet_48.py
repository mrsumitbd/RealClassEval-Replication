
import datetime as dt


class Datetime:

    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        timestamp = int(datetime.timestamp())
        return timestamp.to_bytes(4, byteorder='little')

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        timestamp = int.from_bytes(data, byteorder='little')
        return dt.datetime.fromtimestamp(timestamp)

    @staticmethod
    def now() -> dt.datetime:
        return dt.datetime.now()

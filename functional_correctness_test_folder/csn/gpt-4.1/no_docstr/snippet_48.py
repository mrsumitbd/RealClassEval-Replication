
import datetime as dt


class Datetime:

    @staticmethod
    def pack(datetime_obj: dt.datetime) -> bytes:
        # Use ISO format and encode as UTF-8
        return datetime_obj.isoformat().encode('utf-8')

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        # Decode and parse from ISO format
        return dt.datetime.fromisoformat(data.decode('utf-8'))

    @staticmethod
    def now() -> dt.datetime:
        return dt.datetime.now()

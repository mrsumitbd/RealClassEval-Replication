import datetime as dt


class Datetime:

    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        return datetime.isoformat().encode("utf-8")

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        return dt.datetime.fromisoformat(data.decode("utf-8"))

    @staticmethod
    def now() -> dt.datetime:
        return dt.datetime.now(dt.timezone.utc)


import datetime as dt
import struct


class Datetime:
    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        """
        Pack a datetime object into 8 bytes representing the POSIX timestamp
        as a big‑endian double precision float.
        """
        if datetime.tzinfo is not None:
            # Convert to UTC for a consistent timestamp
            datetime = datetime.astimezone(
                dt.timezone.utc).replace(tzinfo=None)
        ts = datetime.timestamp()
        return struct.pack('>d', ts)

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        """
        Unpack 8 bytes into a datetime object. The bytes must represent a
        big‑endian double precision float timestamp.
        """
        if len(data) != 8:
            raise ValueError("Data must be exactly 8 bytes long")
        ts = struct.unpack('>d', data)[0]
        return dt.datetime.fromtimestamp(ts)

    @staticmethod
    def now() -> dt.datetime:
        """
        Return the current local datetime.
        """
        return dt.datetime.now()

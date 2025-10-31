
import datetime as dt
import struct


class Datetime:
    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        """Pack a datetime object into 4‑byte little‑endian timestamp."""
        # Convert to POSIX timestamp (seconds since epoch)
        ts = int(datetime.timestamp())
        # Pack as unsigned 32‑bit little‑endian integer
        return struct.pack("<I", ts)

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        """Unpack a 4‑byte little‑endian timestamp received over the Broadlink protocol."""
        if len(data) != 4:
            raise ValueError("Timestamp data must be exactly 4 bytes long")
        # Unpack as unsigned 32‑bit little‑endian integer
        ts = struct.unpack("<I", data)[0]
        # Convert back to datetime
        return dt.datetime.fromtimestamp(ts)

    @staticmethod
    def now() -> dt.datetime:
        """Return the current local datetime."""
        return dt.datetime.now()

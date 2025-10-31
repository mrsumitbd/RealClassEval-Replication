class Datetime:

    @staticmethod
    def pack(datetime) -> bytes:
        import struct
        import datetime as dt
        if not isinstance(datetime, dt.datetime):
            raise TypeError("datetime must be a datetime.datetime instance")
        # Use Unix time (seconds) as 4-byte little-endian
        ts = int(datetime.timestamp())
        if ts < 0:
            raise ValueError("datetime is before Unix epoch")
        return struct.pack("<I", ts)

    @staticmethod
    def unpack(data: bytes):
        '''Unpack a timestamp received over the Broadlink protocol.'''
        import struct
        import datetime as dt

        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")

        n = len(data)

        # 4 bytes: Unix epoch seconds, little-endian
        if n == 4:
            ts = struct.unpack("<I", data)[0]
            return dt.datetime.fromtimestamp(ts)

        # 6 bytes: [year-2000, month, day, hour, minute, second]
        if n == 6:
            y = 2000 + data[0]
            m, d, hh, mm, ss = data[1], data[2], data[3], data[4], data[5]
            return dt.datetime(y, m, d, hh, mm, ss)

        # 7 bytes: [year_low, year_high, month, day, hour, minute, second]
        if n == 7:
            y = data[0] | (data[1] << 8)
            m, d, hh, mm, ss = data[2], data[3], data[4], data[5], data[6]
            return dt.datetime(y, m, d, hh, mm, ss)

        # 8 bytes: try unsigned 64-bit epoch
        if n == 8:
            val = struct.unpack("<Q", data)[0]
            # Heuristic: if value looks like milliseconds, convert; else treat as seconds
            if val > 10**12:
                return dt.datetime.fromtimestamp(val / 1000.0)
            return dt.datetime.fromtimestamp(val)

        raise ValueError(f"Unsupported timestamp length: {n}")

    @staticmethod
    def now():
        import datetime as dt
        return dt.datetime.now()

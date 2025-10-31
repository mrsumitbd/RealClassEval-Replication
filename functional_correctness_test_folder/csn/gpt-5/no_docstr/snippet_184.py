class Encoder:
    _UNRESERVED = set(
        b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~"
    )

    def needsEncoding(self, s):
        if not isinstance(s, str):
            raise TypeError("s must be a string")
        for b in s.encode("utf-8"):
            if b not in self._UNRESERVED:
                return True
        return False

    def encode(self, s):
        if not isinstance(s, str):
            raise TypeError("s must be a string")
        out = []
        for b in s.encode("utf-8"):
            if b in self._UNRESERVED:
                out.append(chr(b))
            else:
                out.append("%{:02X}".format(b))
        return "".join(out)

    def decode(self, s):
        if not isinstance(s, str):
            raise TypeError("s must be a string")
        out_bytes = bytearray()
        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == "%":
                if i + 2 >= n:
                    raise ValueError(
                        "Incomplete percent-encoding at end of string")
                h1 = s[i + 1]
                h2 = s[i + 2]
                try:
                    val = int(h1 + h2, 16)
                except ValueError:
                    raise ValueError(
                        f"Invalid percent-encoding '%{h1}{h2}' at position {i}")
                out_bytes.append(val)
                i += 3
            else:
                # Allow raw non-ASCII in input; encode to UTF-8 bytes
                out_bytes.extend(ch.encode("utf-8"))
                i += 1
        return out_bytes.decode("utf-8")

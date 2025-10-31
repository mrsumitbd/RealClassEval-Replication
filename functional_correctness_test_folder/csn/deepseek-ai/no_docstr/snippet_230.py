
class RawPacket:

    def __init__(self, packet):
        self._packet = packet

    def __getattr__(self, fieldname):
        if fieldname in self._packet:
            return self._packet[fieldname]
        raise AttributeError(
            f"'RawPacket' object has no attribute '{fieldname}'")

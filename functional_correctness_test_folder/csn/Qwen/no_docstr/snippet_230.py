
class RawPacket:

    def __init__(self, packet):
        self.packet = packet

    def __getattr__(self, fieldname):
        if fieldname in self.packet:
            return self.packet[fieldname]
        raise AttributeError(
            f"'RawPacket' object has no attribute '{fieldname}'")

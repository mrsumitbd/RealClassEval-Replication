class PacketContext:
    def __init__(self, packet):
        self.packet = packet

    def __getitem__(self, name):
        if isinstance(self.packet, dict):
            return self.packet[name]
        return getattr(self.packet, name)

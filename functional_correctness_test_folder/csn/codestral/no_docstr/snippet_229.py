
class PacketContext:

    def __init__(self, packet):
        self.packet = packet

    def __getitem__(self, name):
        return getattr(self.packet, name)

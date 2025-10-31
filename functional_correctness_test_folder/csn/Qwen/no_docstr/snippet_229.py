
class PacketContext:

    def __init__(self, packet):
        self.packet = packet
        self.fields = {}
        if isinstance(packet, dict):
            self.fields = packet

    def __getitem__(self, name):
        return self.fields.get(name, None)

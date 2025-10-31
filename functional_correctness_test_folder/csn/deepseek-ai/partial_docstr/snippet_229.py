
class PacketContext:

    def __init__(self, packet):
        '''Creates a new PacketContext for the given Packet.'''
        self.packet = packet
        self.fields = {}

    def __getitem__(self, name):
        return self.fields.get(name, None)


class PacketContext:

    def __init__(self, packet):
        '''Creates a new PacketContext for the given Packet.'''
        self.packet = packet

    def __getitem__(self, name):
        return getattr(self.packet, name)

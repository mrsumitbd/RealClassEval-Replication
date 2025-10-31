
class PacketContext:
    def __init__(self, packet):
        '''Creates a new PacketContext for the given Packet.'''
        self.packet = packet

    def __getitem__(self, name):
        # Try dictionary-style access first
        if isinstance(self.packet, dict):
            return self.packet[name]
        # Fallback to attribute access
        try:
            return getattr(self.packet, name)
        except AttributeError:
            raise KeyError(name)

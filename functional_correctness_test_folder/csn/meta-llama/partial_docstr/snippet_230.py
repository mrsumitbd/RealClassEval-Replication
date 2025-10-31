
class RawPacket:

    def __init__(self, packet):
        self.packet = packet

    def __getattr__(self, fieldname):
        '''Returns the value of the given packet fieldname as a raw
        value with no DN to EU conversion applied.
        '''
        return self.packet.get(fieldname)

from struct import pack, unpack, calcsize

class Packet:
    """Class representing a generic HCI packet.

    :param header: The packet header.
    :type header: bytes
    :returns: Packet instance.
    :rtype: Packet

    """
    'A generic packet that will be build fromparts'

    def __init__(self, header='\x00', fmt='>B'):
        self.header = header
        self.fmt = fmt
        self.payload = []
        self.raw_data = None

    def encode(self):
        return pack(self.fmt, self.header)

    def decode(self, data):
        try:
            if unpack(self.fmt, data[:calcsize(self.fmt)])[0] == self.header:
                self.raw_data = data
                return data[calcsize(self.fmt):]
        except:
            pass
        return None

    def retrieve(self, aclass):
        """Look for a specifc class/name in the packet"""
        resu = []
        for x in self.payload:
            try:
                if isinstance(aclass, str):
                    if x.name == aclass:
                        resu.append(x)
                elif isinstance(x, aclass):
                    resu.append(x)
                resu += x.retrieve(aclass)
            except:
                pass
        return resu
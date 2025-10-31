
from collections.abc import ByteString


class AES_GCM_Mechanism:
    '''CKM_AES_GCM warpping mechanism'''

    def __init__(self, iv, aad, tagBits):
        '''
        :param iv: initialization vector
        :param aad: additional authentication data
        :param tagBits: length of authentication tag in bits
        '''
        if not isinstance(iv, (bytes, bytearray)):
            raise TypeError("iv must be bytes or bytearray")
        if not isinstance(aad, (bytes, bytearray)):
            raise TypeError("aad must be bytes or bytearray")
        if not isinstance(tagBits, int):
            raise TypeError("tagBits must be an integer")
        if tagBits % 8 != 0 or tagBits <= 0:
            raise ValueError("tagBits must be a positive multiple of 8")
        self.iv = bytes(iv)
        self.aad = bytes(aad)
        self.tagBits = tagBits

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            'iv': self.iv,
            'ivLen': len(self.iv),
            'aad': self.aad,
            'aadLen': len(self.aad),
            'tagBits': self.tagBits
        }

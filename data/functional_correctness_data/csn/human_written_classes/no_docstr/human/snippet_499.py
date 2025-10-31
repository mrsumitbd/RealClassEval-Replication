from abc import ABCMeta
from struct import pack

class Message:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @property
    def message_id(self):
        raise NotImplementedError('no default message_id')

    def _bytes_to_message(self, msg):
        if isinstance(msg, list):
            msg = ''.join(msg)
        if hasattr(msg, 'bytesize'):
            bytesize = msg.bytesize + 4
        else:
            bytesize = len(msg) + 4
        message_size = pack('!I', bytesize)
        if self.message_id is not None:
            msg_with_size = self.message_id + message_size + msg
        else:
            msg_with_size = message_size + msg
        return msg_with_size

    def __str__(self):
        return self.__class__.__name__
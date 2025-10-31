
class Mechanism:
    '''Wraps CK_MECHANISM'''

    def __init__(self, mechanism, param=None):
        '''
        :param mechanism: the mechanism to be used
        :type mechanism: integer, any `CKM_*` value
        :param param: data to be used as crypto operation parameter
          (i.e. the IV for some algorithms)
        :type param: string or list/tuple of bytes
        :see: :func:`Session.decrypt`, :func:`Session.sign`
        '''
        self.mechanism = mechanism
        self.param = param

    def to_native(self):
        '''convert mechanism to native format'''
        if self.param is None:
            return (self.mechanism, None)
        elif isinstance(self.param, str):
            return (self.mechanism, self.param.encode('utf-8'))
        elif isinstance(self.param, (list, tuple)):
            return (self.mechanism, bytes(self.param))
        else:
            raise TypeError("param must be a string or list/tuple of bytes")

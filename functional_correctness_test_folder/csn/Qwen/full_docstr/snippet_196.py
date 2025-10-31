
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
        if isinstance(self.param, (list, tuple)):
            self.param = bytes(self.param)
        return {'mechanism': self.mechanism, 'param': self.param}

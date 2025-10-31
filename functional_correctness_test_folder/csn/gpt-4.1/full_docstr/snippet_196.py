
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
        # Simulate a CK_MECHANISM struct as a dict
        native = {
            'mechanism': self.mechanism,
            'parameter': None,
            'parameter_len': 0
        }
        if self.param is not None:
            if isinstance(self.param, (bytes, bytearray)):
                native['parameter'] = self.param
                native['parameter_len'] = len(self.param)
            elif isinstance(self.param, str):
                param_bytes = self.param.encode('utf-8')
                native['parameter'] = param_bytes
                native['parameter_len'] = len(param_bytes)
            elif isinstance(self.param, (list, tuple)):
                # Assume list/tuple of bytes
                param_bytes = bytes(self.param)
                native['parameter'] = param_bytes
                native['parameter_len'] = len(param_bytes)
            else:
                raise TypeError(
                    "param must be bytes, str, list or tuple of bytes")
        return native

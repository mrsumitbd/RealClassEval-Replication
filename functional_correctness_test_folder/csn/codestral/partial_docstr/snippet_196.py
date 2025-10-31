
class Mechanism:
    '''Wraps CK_MECHANISM'''

    def __init__(self, mechanism, param=None):
        self.mechanism = mechanism
        self.param = param

    def to_native(self):
        '''convert mechanism to native format'''
        return (self.mechanism, self.param)

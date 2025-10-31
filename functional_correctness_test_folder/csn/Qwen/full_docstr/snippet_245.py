
class Sampleable:
    '''Element who can provide samples
    '''

    def __init__(self):
        '''Class instantiation
        '''
        self.default_value = None

    def get_sample(self):
        '''Return the a sample for the element
        '''
        return self.default_value

    def get_default_sample(self):
        '''Return default value for the element
        '''
        return self.default_value
